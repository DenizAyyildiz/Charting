from dash import dcc, html
import dash_bootstrap_components as dbc
from valfapp.layouts import nav_bar

layout = [
    nav_bar,
    dbc.Container(
        [
            dbc.Row([
                dbc.Col(
                    html.A(
                        html.Div(
                            "Costing",
                            style={
                                "height": "200px",
                                "border-radius": "10px",
                                "justify-content": "center",
                                "align-items": "center",
                                "display": "flex",
                                "background-color": "white"
                            },
                        ),
                        href="/costing",
                        style={"text-decoration": "none", "color": "#2149b4", "font-size": "24px"},
                    ),
                    className="mt-2 col-lg-4 col-md-6 col-sm-12",
                ),
                dbc.Col(
                    html.A(
                        html.Div(
                            "Tutarlama",
                            style={
                                "height": "200px",
                                "border-radius": "10px",
                                "justify-content": "center",
                                "align-items": "center",
                                "display": "flex",
                                "background-color": "white"
                            },
                        ),
                        href="/value",
                        style={"text-decoration": "none", "color": "#2149b4", "font-size": "24px"},
                    ),
                    className="mt-2 col-lg-4 col-md-6 col-sm-12",
                ),
            ],
                className="justify-content-center align-items-center"),

        ],
        fluid=True,  # Set to True for a fluid layout that fills the available space
    )
]

