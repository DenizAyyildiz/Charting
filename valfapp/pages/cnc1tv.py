import json
from datetime import date, timedelta, datetime

import pandas as pd

from valfapp.app import workcenters, app, prdconf, return_piechart
from valfapp.layouts import layout_for_tvs
import dash_table
from dash import dcc, html, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from config import project_directory
from run.agent import ag
from valfapp.layouts import sliding_indicator_container
from valfapp.app import cache
import plotly.express as px
from dash_ag_grid import AgGrid
from dash_table import DataTable

today = datetime.today()

if today.weekday() == 6:
    kb = 2
elif today.weekday() == 0:
    kb = 3
else:
    kb = 1

params_list = [(date.today() - timedelta(days=kb)).isoformat(), date.today().isoformat(), "day"]



# Define your layouts here
layout1 = layout_for_tvs(costcenter='CNC1')

layout2 = html.Div([
    dbc.Col([
        html.H2("Talaşlı İmalat Planları", style={"text-align": "center", 'fontWeight': 'bold','fontSize': '55px',
                                "color": "white", 'margin-top': '8px', "background-color": "rgba(33, 73, 180, 1)"}),
        DataTable(
            id='table_layout_2',
            columns=[
                {'name': 'İş Merkezi', 'id': 'WORKCENTER'},
                {'name': 'Malzeme', 'id': 'MATERIAL'},
                {'name': 'Resim No.', 'id': 'DRAWNUM'},
                {'name': 'Plan Toplam', 'id': 'BLOCKQTY'},
                {'name': 'Üretim Toplam', 'id': 'PRODUCTBLOCKQTY'},
                {'name': 'Kalan Plan', 'id': 'REMAINPLN'},
                {'name': 'Plan Bitiş', 'id': 'FINISHDAY'},
                {'name': 'Not (Planlama)', 'id': 'STEXT'},
            ],

            style_table={
                'height': '800',
                'overflowY': 'auto',
                'border': 'thin lightgrey solid',
                'fontFamily': 'Arial, sans-serif',
                'minWidth': '100%',  # Adjust this value to set the minimum width
                'width': '100%',  # Adjust this value to set the width
                'textAlign': 'left',
                'color': 'black',
                'background-color': 'white',
                'fontSize': '26px',

            },
            style_header={
                'backgroundColor': 'rgba(0, 0, 0, 0)',  # Semi-transparent background
                'fontWeight': 'bold',  # Bold font
                'color': '#2F4F4F',  # Cool text color
                'fontFamily': 'Arial, sans-serif',  # Font family
                'fontSize': '28px',
                'border': '1px solid  brown',
                'borderRadius': '2px',
                'textAlign': 'center',

            },

            style_data_conditional=[]

        ),

    ], width=15),
])


# Add the new interval component for layout switching
layout = html.Div([
    dcc.Interval(id='layout-switch-interval', interval=180*1000, n_intervals=0),  # Switch every 15 seconds
    html.Div(id='dynamic-layout-container')
])

# Callback to switch between layouts
@app.callback(
    Output('dynamic-layout-container', 'children'),
    Input('layout-switch-interval', 'n_intervals')
)
def switch_layout(n_intervals):
    # Alternate between layout1 and layout2 every 15 seconds
    if n_intervals % 2 == 0:
        return layout1
    else:
        return layout2

# Callback to toggle play/pause state
@app.callback(
    Output("animate_cnc1", "disabled"),
    Input("play", "n_clicks"),
    State("animate_cnc1", "disabled"),
)
def toggle(n, playing):
    print("****888*****")
    print(n)
    if n:
        return not playing
    return playing

# Callback to update the content in layout1
@app.callback(
    Output('graph_layout_1', 'figure'),
    Output('table_layout_1', 'data'),
    Output('table_layout_1', 'columns'),
    Input("animate_cnc1", "n_intervals"),
    Input("wc-slider_cnc1", "value"),
    State(component_id='oeelist1w_tv_cnc1', component_property='data'),
    State(component_id='oeelist3w_tv_cnc1', component_property='data'),
    State(component_id='oeelist7w_tv_cnc1', component_property='data'),
    prevent_initial_call=True,
)
def update_layout1_content(n, selected_value, oeelist1w, oeelist3w, oeelist7w):
    print("buradayız")
    params_dic = {"workstart": (date.today() - timedelta(days=kb)).isoformat(),
                  "workend": date.today().isoformat(),
                  "interval": "day"}

    list_of_figs, list_of_data, list_of_columns, list_of_styles = workcenters("CNC1", "pers", params_dic, oeelist1w,
                                                                              oeelist3w, oeelist7w,1)
    print(" burada mıyız ????? ")
    list_of_figs = [i for i in list_of_figs if i != {}]
    max_of_slider = len(list_of_figs)

    print("asdadasdasda")
    print(list_of_data)
    print("asdadasdasda")

    if selected_value + 1 > len(list_of_figs):
        selected_value = -1
        figure1 = list_of_figs[selected_value]
        data1 = list_of_data[selected_value]
        columns1 = list_of_columns[selected_value]
    else:
        figure1 = list_of_figs[selected_value]
        data1 = list_of_data[selected_value]
        columns1 = list_of_columns[selected_value]

    return figure1, data1, columns1

# Callback to update the content in layout2


@app.callback(
    Output('table_layout_2', 'data'),
    Output('table_layout_2', 'columns'),
    Output('table_layout_2', 'style_data_conditional'),
    Input('layout-switch-interval', 'n_intervals')
)
def update_layout2_content(n):
    # Query data from the database
    data2 = ag.run_query(r"C:\Users\fozturk\Documents\GitHub\Charting\queries\livecnc1plan.sql")
    data2["FINISHDAY"] = pd.to_datetime(data2["FINISHDAY"]).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Sort data by WORKCENTER
    data2 = data2.sort_values(by="WORKCENTER").reset_index(drop=True)

    # Insert black row between different WORKCENTERs
    modified_data = []
    for i, row in data2.iterrows():
        row_dict = row.to_dict()

        # Calculate the bar length based on the ratio of REMAINPLN to BLOCKQTY
        remain_pln = row_dict.get('REMAINPLN', 0)
        block_qty = row_dict.get('BLOCKQTY', 1)  # Avoid division by zero
        bar_length = int((remain_pln / block_qty) * 20)  # Scale bar length between 0 and 20 characters
        bar = '|' * bar_length  # Use '|' to simulate a bar
        row_dict['REMAINPLN'] = f"{remain_pln} {bar}"

        # Append the current row
        modified_data.append(row_dict)

        # Check if the next row has a different WORKCENTER, if so, insert a black row
        if i < len(data2) - 1 and data2.iloc[i]["WORKCENTER"] != data2.iloc[i + 1]["WORKCENTER"]:
            black_row = {col: "" for col in data2.columns}  # Create a blank row
            black_row['WORKCENTER'] = 'BLACK_ROW'  # You can use a special identifier for styling
            modified_data.append(black_row)

    # Rename columns just before returning
    data2.rename(columns={
        "WORKCENTER": "İş Merkezi",
        "MATERIAL": "Malzeme",
        "DRAWNUM": "Resim No.",
        "BLOCKQTY": "Plan Toplam",
        "PRODUCTBLOCKQTY": "Üretim Toplam",
        "REMAINPLN": "Kalan Plan",
        "FINISHDAY": "Plan Bitiş",
        "STEXT": "Not (Planlama)"
    }, inplace=True)

    # Update the modified_data to reflect the new column names
    for row in modified_data:
        if "WORKCENTER" in row:
            row["İş Merkezi"] = row.pop("WORKCENTER")
        if "MATERIAL" in row:
            row["Malzeme"] = row.pop("MATERIAL")
        if "DRAWNUM" in row:
            row["Resim No."] = row.pop("DRAWNUM")
        if "BLOCKQTY" in row:
            row["Plan Toplam"] = row.pop("BLOCKQTY")
        if "PRODUCTBLOCKQTY" in row:
            row["Üretim Toplam"] = row.pop("PRODUCTBLOCKQTY")
        if "REMAINPLN" in row:
            row["Kalan Plan"] = row.pop("REMAINPLN")
        if "FINISHDAY" in row:
            row["Plan Bitiş"] = row.pop("FINISHDAY")
        if "STEXT" in row:
            row["Not (Planlama)"] = row.pop("STEXT")

    # Create column definitions from the DataFrame's columns
    columns = [{"name": col, "id": col} for col in data2.columns]

    # Style the black row conditionally
    style_data_conditional = [
        {
            'if': {'filter_query': '{İş Merkezi} = "BLACK_ROW"'},
            'backgroundColor': 'black',
            'color': 'black',  # Make text black to effectively hide it
            'height': '10px',  # Adjust row height as needed
        },
        # Styling the REMAINPLN (now "Kalan Plan") column to make the bar red
        {
            'if': {'column_id': 'Kalan Plan'},
            'color': 'red',  # Make the bar red
            'textAlign': 'left',
            'fontFamily': 'monospace',  # Use a monospace font to keep the bar's alignment consistent
        },
    ]

    return modified_data, columns, style_data_conditional



# Callback to update individual figures for each work center in the selected cost center
@app.callback(
    Output('wc-output-container_cnc1', 'children'),
    Input("animate_cnc1", "n_intervals"),
    Input("wc-slider_cnc1", "value"),
    State("livedata_cnc1", 'data')
)
def update_ind_fig(n, selected_value, livedata_cnc1):
    return sliding_indicator_container(livedata=livedata_cnc1,
                                       selected_value=selected_value, costcenter='CNC1')

# Callback to refresh data
@app.callback(
    Output("oeelist1w_tv_cnc1", "data"),
    Output('oeelist3w_tv_cnc1', 'data'),
    Output('oeelist7w_tv_cnc1', 'data'),
    Output('oeelist0w_tv_cnc1', 'data'),
    Input("15min_update", "n_intervals"))
def refresh_data(n):
    params_dic = {"workstart": (date.today() - timedelta(days=kb)).isoformat(),
                  "workend": date.today().isoformat(),
                  "interval": "day"}
    cache.delete_memoized(prdconf, (params_dic["workstart"], params_dic["workend"], params_dic["interval"]))
    oeelist1w = prdconf(params_list)[1]
    oeelist3w = prdconf(params_list)[3]
    oeelist7w = prdconf(params_list)[7]
    oeelist0w = prdconf(params_list)[0]
    return  oeelist1w,oeelist3w,oeelist7w,oeelist0w

# Callback to update the pie chart
@app.callback(
    Output('pie_of_yesterday_cnc1', 'figure'),
    Input("oeelist0w_tv_cnc1", "data"),
    Input("play", "n_clicks"))
def update_piechart(oeelist0w, n):
    print(oeelist0w)
    return return_piechart("CNCTORNA", oeelist0w)

if __name__ == '__main__':
    app.run_server(debug=True)
