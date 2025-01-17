import datetime as dt
import pandas as pd
from dash.exceptions import PreventUpdate
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from config import project_directory
import json
from valfapp.functions.functions_prd import indicator_for_tvs, get_daily_qty, working_machinesf, scatter_plot, \
    legend_generater, indicator_with_color, generate_for_sparkline
from dash import dcc, html, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from valfapp.app import app, prdconf, return_piechart, workcenters
from run.agent import ag
import plotly.express as px  # (version 4.7.0 or higher)
from valfapp.configuration import layout_color
import plotly.graph_objs as go
import dash_table

summary_color = 'black'

cur_week = (dt.datetime.now() + relativedelta(months=-1)).strftime('%Y-%U').zfill(6)
try:
    value = int(
        ag.run_query(f"SELECT SUM(VALUE) AS TOTALVAL FROM VLFVALUATION WHERE VALDATE = '{cur_week}'")["TOTALVAL"][0])
except TypeError:

    value = int(12000000)

total_value_with_separator = format(value, ",")

today = datetime.today()

if today.weekday() == 6:
    kb = 2
elif today.weekday() == 0:
    kb = 3
else:
    kb = 1

###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
###### ###### ###### ###### ###### NAV BAR NAV BAR NAV VAR ###### ###### ###### ###
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######


nav_bar = html.Nav(className="main-menu side-bar", children=[
    dbc.Container([
        html.Div(className="logo-div resim-container", children=[
            html.A(className="logo", href="/", children=[
                html.Img(src='./assets/valflogo.png', className="logo")
            ])
        ]),
        html.Div(className="settings"),
        html.Div(id="style-1", className="scrollbar", children=[
            html.Ul(children=[
                html.Li(children=[
                    html.A(href="/", children=[
                        html.Img(src="../assets/home.png", className="nav-icon"),
                        html.Span(className="nav-text nav-text-2", children="MAIN")
                    ])
                ]),
                #html.Li(className="darkerlishadow", children=[
                  #  html.A(href="/value", children=[
                  #      html.Img(src="../assets/tutarlama-icon.PNG", className="nav-icon"),
                  #      html.Span(className="nav-text", children="Tutarlama")
                  #  ])
               # ]),
                html.Li(className="darkerli", children=[
                    html.A(href="/uretimrapor", children=[
                        html.Img(src="../assets/uretim-raporlari-icon.png", className="nav-icon"),
                        html.Span(className="nav-text", children="Üretim Raporları")
                    ])
                ]),
                html.Li(className="darkerli", children=[
                    html.A(href="/liveprd", children=[
                        html.Img(src="../assets/uretim-takip-icon.PNG", className="nav-icon"),
                        html.Span(className="nav-text", children="Üretim Takip")
                    ])
                ]),
                html.Li(className="darkerli", children=[
                    html.A(href="/tvmonitor", children=[
                        html.Img(src="../assets/tvmonitor-ıcon.png", className="nav-icon"),
                        html.Span(className="nav-text", children="Tv Monitor")
                    ])
                ]),
                html.Li(className="darkerli", children=[
                    html.A(href="/kapasite", children=[
                        html.Img(src="../assets/kapaste-removebg-preview.png", className="nav-icon"),
                        html.Span(className="nav-text", children="Kapasite")
                    ])
                ]),
                html.Li(className="darkerli", children=[
                    html.A(href="/energy", children=[
                        html.Img(src="../assets/enerji-removebg-preview.png", className="nav-icon"),
                        html.Span(className="nav-text", children="Energy")
                    ])
                ]),
                html.Li(className="darkerli", children=[
                    html.A(href="/prdenergy", children=[
                        html.Img(src="../assets/prof-enrgy-removebg-preview.png", className="nav-icon"),
                        html.Span(className="nav-text", children="Prod Energy")
                    ])
                ]),
                #html.Li(className="darkerli", children=[
                  #  html.A(href="/kameraayiklama", children=[
                  #      html.Img(src="../assets/k-ayıklama-removebg-preview.png", className="nav-icon"),
                  #      html.Span(className="nav-text", children="Kam. Ayıklama")
                  #  ])
                #]),
                html.Li(className="darkerli", children=[
                    html.A(href="/kalite", children=[
                        html.Img(src="../assets/kaliteikon.png", className="nav-icon"),
                        html.Span(className="nav-text", children="kalite")
                    ])
                ]),
                html.Li(className="darkerli", children=[
                    html.A(href="/satismuhasebe", children=[
                        html.Img(src="../assets/muhasebeikon.png", className="nav-icon"),
                        html.Span(className="nav-text", children="satismuhasebe")
                    ])
                ]),
                html.Label("Valfsan Engineers © 2024 ", id="signature-label", className="float-left signature-label-sb")
            ]),
        ]),
    ]),
])

###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
###### ###### ###### ###### ######   VALUATION LAYOUTS  ###### ###### ###### ######
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######

layout_27 = dbc.Container([
    dbc.Row(dcc.Link(
        children='Main Page',
        href='/',
        style={"height": 40, "color": "black", "font-weight": "bold"}

    )),
    dbc.Row(html.Button(id='year', value="2022", children='Click me')),
    dbc.Row([

        dbc.Col([html.Div(dcc.Graph(id="piec", figure={}, style={"margin-top": 20}))],
                style={"width": 300, "height": 500, "border-right": "6px black inset"}),

        dbc.Col(html.Div(children=[html.Div(["Current Value", html.Br(), total_value_with_separator],
                                            style={'margin-top': 50, 'margin-left': 100,
                                                   "fontSize": 24,
                                                   "text-align": "center", "color": "white",
                                                   "font-weight": "bold",
                                                   "background-color": "firebrick",
                                                   "height": 70,
                                                   "width": 300}),
                                   html.Br(),
                                   dcc.Graph(id="linechart", figure={},
                                             style={"margin-top": 1, 'margin-right': 520})],
                         style={"height": 100, "width": 250})),
        dbc.Col(html.Div(children=[html.Div(children=[
            html.Button(id='rawmat', n_clicks=0,
                        children='Raw Material'),
            html.Button(id='prod', n_clicks=0,
                        children='Product'),
            html.Button(id='halfprod', n_clicks=0,
                        children='Half Product'),
            html.Button(id='main', n_clicks=0, children='General',

                        style={"margin-left": 0, "color": '#cd5c5c',
                               "background-color": "#FFEBCD"}),
        ],
            style={"margin-top": 50,
                   "background-color": "burlywood"})
        ], style={}))],
        style={"background-color": "#FFEBCD", "width": 1900, "height": 500}),
    dbc.Row(
        [

            html.Div(children=["Div 1", html.Div(dcc.Graph(id="MAMÜL",
                                                           figure={}))],
                     style={"background-color": "#FFEBCD", "width": 944, "height": 600,
                            "margin-top": 9}),

            html.Div(children=["Div 2", html.Div(dcc.Graph(id="HAMMADDE",
                                                           figure={}))],
                     style={"background-color": "#FFEBCD", "width": 944, "height": 600,
                            "margin-left": 6,
                            "margin-top": 9})

        ]
    ),
    dbc.Row(
        [
            html.Div(children=["Div 1", html.Div(dcc.Graph(id="YARI MAMÜL",
                                                           figure={}))],
                     style={"background-color": "#FFEBCD", "width": 944,
                            "height": 600,
                            "margin-top": 1, }),
            html.Div(children=["Div 2", html.Div(dcc.Graph(id="YARDIMCI MALZEME",
                                                           figure={}))],
                     style={"background-color": "#FFEBCD", "width": 944,
                            "height": 600,
                            "margin-left": 6,
                            "margin-top": 1, })

        ], style={"margin-top": 15}
    )
], fluid=True
)

###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######


layout_12 = dbc.Container([
    nav_bar,

    dbc.Row(html.Div(html.Button(id='year', value="2022", children='Click me'), hidden=True)),
    dbc.Row(
        html.Div(
            ["Current Value", html.Br(), total_value_with_separator],
            style={
                'margin-top': 5,
                "padding": 50,
                "fontSize": 30,
                "text-align": "center",
                "color": 'white',
                "font-weight": "bold",
                # "background-color": "#FFEBCD",
                "height": 120,
                "width": 300,
                "display": "flex",  # Enable flexbox
                "justify-content": "center",  # Center horizontally
                "align-items": "center"  # Center vertically
            }
        ),
        style={
            "display": "flex",
            "justify-content": "center"  # Center the div within the row
        }
    ),
    dbc.Row([
        dbc.Col([html.Div(dcc.Graph(id="piec", figure={},
                                    style={"margin-top": 20, "margin-left": "150px", "background-color": "#FFEBCD"}))],
                width=5),
        dbc.Col(
            html.Div(children=[
                html.Button(id='rawmat', n_clicks=0, children='Raw Material',
                            style={"margin-left": 180, "color": '#cd5c5c', "background-color": "#FFEBCD"}),
                html.Button(id='prod', n_clicks=0, children='Product',
                            style={"margin-left": 0, "color": '#cd5c5c', "background-color": "#FFEBCD"}),
                html.Button(id='halfprod', n_clicks=0, children='Half Product',
                            style={"margin-left": 0, "color": '#cd5c5c', "background-color": "#FFEBCD"}),
                html.Button(id='main', n_clicks=0, children='General',
                            style={"margin-left": 0, "color": '#cd5c5c', "background-color": "#FFEBCD"}),
                html.Br(),
                dcc.Graph(id="linechart", figure={}, style={"margin-top": 1, "background-color": "#FFEBCD"}),
            ]),
            style={"height": 100},
            width=6
        )
    ], style={"margin-top": 15}),  # Missing bracket was added here
    dbc.Row([
        dbc.Col(children=[html.Div(dcc.Graph(id="MAMÜL", figure={}))],
                style={"background-color": "#FFEBCD", "margin-top": 9}, width=5),
        dbc.Col(children=[html.Div(dcc.Graph(id="HAMMADDE", figure={}))],
                style={"background-color": "#FFEBCD", "margin-top": 9}, width=5)
    ], style={"justify-content": "center", "align-items": "center", "margin-top": "10px"}),
    dbc.Row([
        dbc.Col(
            children=[html.Div(dcc.Graph(id="YARI MAMÜL", figure={})),
                      ],
            style={"background-color": "#FFEBCD"},
            width=5
        ),
        dbc.Col(
            children=[html.Div(dcc.Graph(id="YARDIMCI MALZEME", figure={}))],
            style={"background-color": "#FFEBCD"},
            width=5
        )
    ], style={"justify-content": "center", "align-items": "center", "margin-top": "10px"})

], fluid=True)

###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
###### ###### ###### ###### ###### MAIN PAGE LAYOUTS ###### ###### ###### ###### ######
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######

layout_12_loginpage_v2 = html.Div(children=[
    nav_bar,

    dbc.Container(children=[
        dbc.Row(
            [
              #  dbc.Col(
               #     html.A(
                 #       html.Div(
                 #           "Tutarlama",
                 ##           style={
                  #              "height": "200px",
                  #              "border-radius": "10px",
                  #              "justify-content": "center",
                  #              "align-items": "center",
                  #              "display": "flex",
                   #             "background-color": "white"
                   #         }, className="deneme"
                   #     ),
                   #     href="/value", style={"text-decoration": "none", "color": "#2149b4", "font-size": "24px"},
                  #  ), className="mt-2 col-lg-3 col-md-7 col-sm-12",
               # ),
                dbc.Col(
                    html.A(
                        html.Div(
                            "Üretim Raporları",
                            style={
                                "height": "200px",
                                "border-radius": "10px",
                                "justify-content": "center",
                                "align-items": "center",
                                "display": "flex",
                                "background-color": "white"
                            },
                        ),
                        href="/uretimrapor", style={"text-decoration": "none", "color": "#2149b4", "font-size": "24px"},
                    ), className="mt-2 col-lg-3 col-md-7 col-sm-12 link-hover",
                ),
                dbc.Col(
                    html.A(
                        html.Div(
                            "Canlı Takip",
                            style={
                                "height": "200px",
                                "border-radius": "10px",
                                "justify-content": "center",
                                "align-items": "center",
                                "display": "flex",
                                "background-color": "white"
                            },
                        ),
                        href="/liveprd", style={"text-decoration": "none", "color": "#2149b4", "font-size": "24px"},
                    ), className="mt-2 col-lg-3 col-md-7 col-sm-12 link-hover",
                ),
                dbc.Col(
                    html.A(
                        html.Div(
                            "TV Monitor",
                            style={
                                "height": "200px",
                                "border-radius": "10px",
                                "justify-content": "center",
                                "align-items": "center",
                                "display": "flex",
                                "background-color": "white",
                            },
                        ),
                        href="/tvmonitor", style={"text-decoration": "none", "color": "#2149b4", "font-size": "24px"},
                    ), className="mt-2 col-lg-3 col-md-7 col-sm-12 link-hover",
                ),
                dbc.Col(
                    html.A(
                        html.Div(
                            "Satış-Muhasebe",
                            style={
                                "height": "200px",
                                "border-radius": "10px",
                                "justify-content": "center",
                                "align-items": "center",
                                "display": "flex",
                                "background-color": "white"
                            }, className="deneme"
                        ),
                        href="/satismuhasebe", style={"text-decoration": "none", "color": "#2149b4", "font-size": "24px"},
                    ), className="mt-2 col-lg-3 col-md-7 col-sm-12",
                ),
                dbc.Col(
                    html.A(
                        html.Div(
                            "Enerji Ölçüm",
                            style={
                                "height": "200px",
                                "border-radius": "10px",
                                "justify-content": "center",
                                "align-items": "center",
                                "display": "flex",
                                "background-color": "white"
                            },
                        ),
                        href="/energy", style={"text-decoration": "none", "color": "#2149b4", "font-size": "24px"},
                    ), className="mt-2 col-lg-3 col-md-7 col-sm-12 link-hover",
                ),
                dbc.Col(
                    html.A(
                        html.Div(
                            "Kapasite (Geliştiriliyor)",
                            style={
                                "height": "200px",
                                "border-radius": "10px",
                                "justify-content": "center",
                                "align-items": "center",
                                "display": "flex",
                                "background-color": "white"
                            },
                        ),
                        href="/kapasite", style={"text-decoration": "none", "color": "#2149b4", "font-size": "24px"},
                    ), className="mt-2 col-lg-3 col-md-7 col-sm-12 link-hover",
                ),
                dbc.Col(
                    html.A(
                        html.Div(
                            "Kalite",
                            style={
                                "height": "200px",
                                "border-radius": "10px",
                                "justify-content": "center",
                                "align-items": "center",
                                "display": "flex",
                                "background-color": "white"
                            }, className="deneme"
                        ),
                        href="/kalite", style={"text-decoration": "none", "color": "#2149b4", "font-size": "24px"},
                    ), className="mt-2 col-lg-3 col-md-7 col-sm-12",
                ),





            ], style={"justify-content": "center", "align-items": "center", }

 )
    ], )
])

layout_12_loginpage = dbc.Container([
    dbc.Row([
        dbc.Col(
            children=[
                html.Div(
                    html.Img(src='assets/valfsan_logo2.png', className="valfsan-logo"),
                )
            ],
            width={"size": 12}
        )
    ],
        className="container-fluid",
        style={"background-color": "rgba(187, 187, 187, 0.289)"}),

    dbc.Row([
        dbc.Col(
            html.Div(
                className="row justify-content-center",
                children=[
                    dcc.Link(
                        html.Div(
                            className="mt-2 justify-content-center",
                            style={
                                'border': '1px solid red',
                                'width': '300px',
                                'height': '200px',
                                'borderRadius': '10px',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'background-color': 'lightgray',
                            },
                            children=[
                                html.Div(
                                    style={
                                        'font-size': '18px',
                                        'color': 'White',
                                        'position': 'absolute',
                                        "border-radius": "20px"
                                    },
                                    children=""
                                ),
                                html.Img(
                                    src='/assets/Tutarlama.png',
                                )
                            ],
                        ),
                        href='/value', style={"width": "310px"},
                    )
                ]
            ),
            className="mt-2 col-lg-3 col-md-6 col-sm-12",
        ),
        dbc.Col(
            html.Div(
                className="row justify-content-center",
                children=[
                    dcc.Link(
                        html.Div(
                            className="mt-2 justify-content-center",
                            style={
                                'border': '1px solid red',
                                'width': '300px',
                                'height': '200px',
                                'borderRadius': '10px',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'background-color': 'lightgray',
                            },
                            children=[
                                html.Div(
                                    style={
                                        'font-size': '18px',
                                        'color': 'White',
                                        'position': 'absolute',
                                        "border-radius": "20px"
                                    },
                                    children=""
                                ),
                                html.Img(
                                    src='/assets/Üretim Raporları.png',
                                )
                            ],
                        ),
                        href='/uretimrapor', style={"width": "310px"},
                    )
                ]
            ),
            className="mt-2 col-lg-3 col-md-6 col-sm-12",
        ),
        dbc.Col(
            html.Div(
                className="row justify-content-center",
                children=[
                    dcc.Link(
                        html.Div(
                            className="mt-2 justify-content-center",
                            style={
                                'border': '1px solid red',
                                'width': '300px',
                                'height': '200px',
                                'borderRadius': '10px',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'background-color': 'lightgray',
                            },
                            children=[
                                html.Div(
                                    style={
                                        'font-size': '18px',
                                        'color': 'White',
                                        'position': 'absolute',
                                        "border-radius": "20px"
                                    },
                                    children=""
                                ),
                                html.Img(
                                    src='/assets/Yislem.png',
                                )
                            ],
                        ),
                        href='/deneme', style={"width": "310px"},
                    )
                ]
            ),
            className="mt-2 col-lg-3 col-md-6 col-sm-12",
        ),
        dbc.Col(
            html.Div(
                className="row justify-content-center",
                children=[
                    dcc.Link(
                        html.Div(
                            className="mt-2 justify-content-center",
                            style={
                                'border': '1px solid red',
                                'width': '300px',
                                'height': '200px',
                                'borderRadius': '10px',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'background-color': 'lightgray',
                                'background-image': '/assets/Taslama.png',
                            },
                            children=[
                                html.Div(
                                    style={
                                        'font-size': '18px',
                                        'color': 'White',
                                        "border-radius": "20px"
                                    },
                                    children=""
                                ),
                                html.Img(
                                    src='/assets/Üretim takip.png',
                                )
                            ],
                        ),
                        href='/liveprd', style={"width": "310px"},
                    )
                ]
            ),
            className="mt-2 col-lg-3 col-md-6 col-sm-12",
        ),
    ], className="mt-5"),

    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    className="row justify-content-center",
                    children=[
                        dcc.Link(
                            html.Div(
                                className="mt-2 justify-content-center",
                                style={
                                    # 'border': '1px solid red',
                                    'width': '300px',
                                    'height': '200px',
                                    'borderRadius': '10px',
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'justifyContent': 'center',
                                    'background-color': 'lightgray',
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'font-size': '18px',
                                            'color': 'White',
                                            'position': 'absolute',
                                            "border-radius": "20px"
                                        },
                                        children=""
                                    ),
                                    html.Img(
                                        src='/assets/TV-Monitor.png',
                                    )
                                ],
                            ),
                            href='/tvmonitor', style={"width": "310px"},
                        )
                    ]
                ),
                className="mt-2 col-lg-3 col-md-6 col-sm-12",
            ),
            dbc.Col(
                html.Div(
                    className="row justify-content-center",
                    children=[
                        dcc.Link(
                            html.Div(
                                className="mt-2 justify-content-center",
                                style={
                                    # 'border': '1px solid red',
                                    'width': '300px',
                                    'height': '200px',
                                    'borderRadius': '10px',
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'justifyContent': 'center',
                                    'background-color': 'lightgray',
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'font-size': '18px',
                                            'color': 'White',
                                            'position': 'absolute',
                                            "border-radius": "20px"
                                        },
                                        children=""
                                    ),
                                    html.Img(
                                        src='/assets/enerji.png',
                                    )
                                ],
                            ),
                            href='/energy', style={"width": "310px"},
                        ),
                        dcc.Link(
                            html.Div(
                                className="mt-2 justify-content-center",
                                style={
                                    # 'border': '1px solid red',
                                    'width': '300px',
                                    'height': '200px',
                                    'borderRadius': '10px',
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'justifyContent': 'center',
                                    'background-color': 'lightgray',
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'font-size': '18px',
                                            'color': 'White',
                                            'position': 'absolute',
                                            "border-radius": "20px"
                                        },
                                        children=""
                                    ),
                                    html.Img(
                                        src='/assets/enerji.png',
                                    )
                                ],
                            ),
                            href='/energy', style={"width": "310px"},
                        )
                    ]
                ),
                className="mt-2 col-lg-3 col-md-6 col-sm-12",
            ),
        ], style={'justify-content': 'center'}, className='mt-5',
    ),
    dcc.Link(
        children='Kamera Ayıklama Sonuçlar',
        href='/camayik',
    ),
    dcc.Link(
        children='Kamera Ayıklama Üretim Raporu',
        href='/camayikuretim',
    ),
    dcc.Link(
        children='Kamera Ayıklama Üretim Takip ',
        href='/livekamera',
    ),
], style={"height": "100vh", "position": "relative"}, fluid=True)

###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######

layout_27_loginpage = dbc.Container([
    # dcc.Interval(
    #     id='interval-component',
    #     interval=1000000, # 5000 milliseconds = 5 seconds
    #     n_intervals=0
    # ),
    dbc.Row([html.H1("Valfsan Analytics",
                     style={"text-align": "center", 'color': 'LightSteelBlue', 'font-weight': 'bold',
                            'padding': 50,
                            "width": 1000, "height": 100})],
            className="justify-content-center"),
    dbc.Row([
        dbc.Col(
            dcc.Link(
                children=[
                    html.Div([
                        html.Img(src='/assets/tutarlama.link.png',
                                 style={"width": "600px", "height": "400px", "object-fit": "fit"}),
                        html.H1("Tutarlama ( Geliştirme Aşamasında )", style={
                            "position": "absolute",
                            "bottom": 8,
                            "right": 8,
                            'color': 'white',
                            'font-weight': 'bold',
                        })
                    ], style={"position": "relative", "display": "inline-block", "box-shadow": "5px 10px #ffffff",
                              "background": "linear-gradient(to bottom right, #cccccc, #323334)"})
                ],
                href='/pg1',
            ),
            width=4,  # Adjust the width of the column, you can use values from 1 to 12
            style={"padding": 14, 'margin-left': 50}
        ),
        dbc.Col(
            dcc.Link(
                children=[
                    html.Div([
                        html.Img(src='/assets/report.link.png',
                                 style={"width": "600px", "height": "400px", "object-fit": "fit"}),
                        html.H1("M.Merkezi OEE Raporu", style={
                            "position": "absolute",
                            "bottom": 8,
                            "right": 8,
                            'color': 'white',
                            'font-weight': 'bold',
                        })
                    ], style={"position": "relative", "display": "inline-block"})
                ],
                href='/prod_eff',
            ),
            width=5,  # Adjust the width of the column, you can use values from 1 to 12
            style={"padding-top": 13, 'margin-left': 43}

        ),
    ], style={'margin-left': 270, 'margin-top': 37, 'margin-bottom': '-45px'}),
    dbc.Row([
        dbc.Col(
            dcc.Link(
                children=[
                    html.Div([
                        html.Img(src='/assets/wc.link.png',
                                 style={"width": "600px", "height": "400px", "object-fit": "fit"}),
                        html.H1("İş Merkezi Raporu", style={
                            "position": "absolute",
                            "bottom": 0,
                            "right": 10,
                            'color': 'white',
                            'font-weight': 'bold',
                        })
                    ], style={"position": "relative", "display": "inline-block"})
                ],
                href='/wcreport',
            ),
            width=4,  # Adjust the width of the column, you can use values from 1 to 12
            style={"padding-top": 30},
        ),
        dbc.Col(
            dcc.Link(
                children=[
                    html.Div([
                        html.Img(src='/assets/live.link.png',
                                 style={"width": "600px", "height": "400px", "object-fit": "fit"}),
                        html.H1("Üretim Canlı Takip", style={
                            "position": "absolute",
                            "bottom": 0,
                            "right": 8,
                            'color': 'white',
                            'font-weight': 'bold',
                        })
                    ], style={"position": "absolute", "display": "inline-block"})
                ], href='/liveprd'),
            width=5,  # Adjust the width of the column, you can use values from 1 to 12
            style={"padding": 28, 'margin-left': 42, 'margin-top': 2}
        ),
    ], style={'margin-left': 322}),
    dcc.Link(
        children='dragtester',
        href='/dragtester',
    )
], fluid=True)


def sliding_indicator_container(livedata, selected_value, costcenter, border='2px solid white'):
    """

    Parameters
    ----------
    livedata: data source of  indicator data
    selected_value: current page of indicator groups
    costcenter: coscenter ( can be another filter of data ) to show

    Returns
    -------
    div of indicators group of 4 with line.

    """
    df = pd.read_json(livedata, orient='split')

    if costcenter == 'CNC1':
        df = df[df["WORKCENTER"].isin(["CNC-07", "CNC-19", "CNC-26", "CNC-28", "CNC-08", "CNC-29"])].reset_index(
            drop=True)
    elif costcenter == 'CNC2':
        df = df[df["WORKCENTER"].isin(
            ["CNC-01", "CNC-03", "CNC-04", "CNC-11", "CNC-12", "CNC-13", "CNC-14", "CNC-15", "CNC-16",
             "CNC-17", "CNC-18",
             "CNC-20", "CNC-21", "CNC-22", "CNC-23"])].reset_index(drop=True)
        print(df["WORKCENTER"].unique())
    else:
        df = df[df["COSTCENTER"] == costcenter].reset_index(drop=True)

    list_of_figs = []
    list_of_stationss = []

    if costcenter == 'CNC1':
        list_of_stationss = ["CNC-07", "CNC-19", "CNC-26", "CNC-28", "CNC-08", "CNC-29"]
    elif costcenter == 'CNC2':
        list_of_stationss = ["CNC-01", "CNC-03", "CNC-04", "CNC-11", "CNC-12", "CNC-13", "CNC-14", "CNC-15", "CNC-16",
                             "CNC-17", "CNC-18",
                             "CNC-20", "CNC-21", "CNC-22", "CNC-23"]
    else:
        for item in df.loc[df["COSTCENTER"] == costcenter]["WORKCENTER"].unique():
            list_of_stationss.append(item)

    for index, row in df.iterrows():
        if index < len(list_of_stationss):
            fig = indicator_for_tvs(row["STATUSR"], row["FULLNAME"], row["WORKCENTER"], row["DRAWNUM"],
                                    row["STEXT"], 0, size={"width": 310, "height": 500}, rate=3 / 4)
            list_of_figs.append(fig)
        else:
            fig = {}
            style = {"display": "none"}

    lengthof = len(list_of_figs)
    x = lengthof % 6
    newlengthof = lengthof - x
    numofforths = newlengthof / 6
    counter = 0

    listofdivs = []
    for i in range(0, len(list_of_figs), 6):
        if counter != numofforths:
            listofdivs.append(html.Div([
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=list_of_figs[i]), style={
                        'border': border}, width=3),
                    dbc.Col(html.Div(children=[dcc.Graph(figure=list_of_figs[i + 1])], style={
                        'border': border}), width=3),
                    dbc.Col(html.Div(children=[dcc.Graph(figure=list_of_figs[i + 2])], style={
                        'border': border}), width=3)
                ], className="g-0"),
                dbc.Row([
                    dbc.Col(html.Div(children=[dcc.Graph(figure=list_of_figs[i + 3])], style={
                        'border': border}), width=3),
                    dbc.Col(html.Div(children=[dcc.Graph(figure=list_of_figs[i + 4])], style={
                        'border': border}), width=3),
                    dbc.Col(html.Div(children=[dcc.Graph(figure=list_of_figs[i + 5])], style={
                        'border': border}), width=3),
                ], className="g-0")
            ]))
        else:
            if x == 0:
                continue
            else:
                print("here")
                listofdivs.append(html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(figure=list_of_figs[i])), width=3),
                        dbc.Col(html.Div(dcc.Graph(figure=list_of_figs[i + 1] if x > 1 else {})), width=3),
                        dbc.Col(html.Div(dcc.Graph(figure=list_of_figs[i + 2] if x > 2 else {})), width=3)
                    ], className="g-0"),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(figure=list_of_figs[i + 3] if x > 3 else {})), width=3),
                        dbc.Col(html.Div(dcc.Graph(figure=list_of_figs[i + 4] if x > 4 else {})), width=3),
                        dbc.Col(html.Div(dcc.Graph(figure=list_of_figs[i + 5] if x > 5 else {})), width=3)
                    ], className="g-0")
                ]))
        counter = counter + 1

    selected_value = selected_value % len(listofdivs)

    return listofdivs[selected_value]


def layout_for_tvs(costcenter='MONTAJ'):
    print(f"pie_of_yesterday_{costcenter.lower()}")
    return [
        dcc.Store(id=f'oeelist1w_tv_{costcenter.lower()}',
                  data=prdconf(((date.today() - timedelta(days=kb)).isoformat(),
                                date.today().isoformat(), "day"))[1]),
        dcc.Store(id=f'oeelist3w_tv_{costcenter.lower()}',
                  data=prdconf(((date.today() - timedelta(days=kb)).isoformat(),
                                date.today().isoformat(), "day"))[
                      3]),
        dcc.Store(id=f'oeelist0w_tv_{costcenter.lower()}',
                  data=prdconf(((date.today() - timedelta(days=kb)).isoformat(),
                                date.today().isoformat(), "day"))[
                      0]),
        dcc.Store(id=f'oeelist7w_tv_{costcenter.lower()}',
                  data=prdconf(((date.today() - timedelta(days=kb)).isoformat(),
                                date.today().isoformat(), "day"))[
                      7]),
        # First Column
        dbc.Row([
            dbc.Col([
                html.Div(id=f"wc-output-container_{costcenter.lower()}", className="row g-0"),
                # Other components for this column
            ], width=8),

            # Second Column
            dbc.Col([
                dbc.Row([
                    dcc.Graph(id=f"pie_of_yesterday_{costcenter.lower()}", style={'margin-left': '-60px'})
                ], className="g-0"),
                dbc.Row([
                    html.Button("Play", id="play", style={'width': '45px'}),
                    dcc.Slider(
                        min=0,
                        max=15,
                        step=1,
                        value=0,
                        id=f'wc-slider_{costcenter.lower()}',
                        className='slider'
                    ),
                    html.Div(
                        id=f'slider-output-container_{costcenter.lower()}',
                        style={'width': 500, 'display': 'inline-block'}),
                    dcc.Interval(id=f"animate_{costcenter.lower()}", interval=10000, disabled=False),
                    dcc.Interval(id="15min_update", interval=80000, disabled=False),
                    dcc.Store(id="list_of_stationss"),
                    dcc.Store(
                        id=f"livedata_{costcenter.lower()}",
                        data=ag.run_query(project_directory + r"\Charting\queries\liveprd.sql").to_json(
                            date_format='iso',
                            orient='split')
                    ),
                ], className="g-0"),
            ], width=4),
        ], className="g-0")]


def return_adr_layout(costcenter='cnc', interval='day',position= '200px'):

    header = 'Haftalık' if interval == 'week' else ( 'Aylık' if interval == 'month' else 'Günlük' )
    # Main Layout
    return dbc.Container([

        dcc.Store(id=f'trigger-timestamp_{costcenter}_{interval}_{position}', data=None),
        # Stores the timestamp of the initial trigger
        dcc.Interval(
            id=f'check-interval_{costcenter}_{interval}_{position}',
            interval=60 * 1000,  # Check every minute
            n_intervals=0
        ),
        dcc.Interval(
            id=f'interval-trigger_{costcenter}_{interval}_{position}',
            interval=1000,  # 1 second
            n_intervals=0,
            max_intervals=1  # Trigger once initially
        ),
        dcc.Store(id=f'oeeelist0_{costcenter}_{interval}_{position}'),
        dcc.Store(id=f'oeeelist1_{costcenter}_{interval}_{position}'),
        dcc.Store(id=f'oeeelist2_{costcenter}_{interval}_{position}'),
        dcc.Store(id=f'oeeelist3_{costcenter}_{interval}_{position}'),
        dcc.Store(id=f'oeeelist5_{costcenter}_{interval}_{position}'),
        dcc.Store(id=f'oeeelist6_{costcenter}_{interval}_{position}'),
        dcc.Store(id=f'oeeelist7_{costcenter}_{interval}_{position}'),

        dcc.Store(id=f'work-dates_{costcenter}_{interval}_{position}'),

        dbc.Row([
            dbc.Col(html.H2(f"{costcenter.upper()} {header} Bölüm Raporu", style={
            "background-color": "#2149b4",
            "text-align": "center",
            "color": "white",
            "padding": "10px",
            "margin-bottom": "20px",
            "border-radius": "5px",
            "font-family": "Arial, sans-serif",
            "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)"
        }))
        ]),
        dbc.Row([
            dbc.Col(html.H5(id=f'valid_data_{costcenter}_{interval}_{position}'))
        ]),

        dbc.Row( dbc.Row() if interval == 'day' else
        [dbc.Row(
            justify="center",
            align="center",
            children=[
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.Div(
                                    className="row text-center text-light",
                                    children=[
                                        dbc.Col(html.H3("Genel Tezgah Verimliliği"),
                                                className="bg-primary col-lg-7 ic-yazilar"),
                                        dbc.Col([
                                            html.H3(id=f'availability_{costcenter}_{interval}_{position}'),
                                            html.P("Hedef %80")
                                        ], className="bg-warning col-lg-5 ic-yazilar-2 p-2")
                                    ]
                                )
                            ),
                            dbc.CardBody(
                                dcc.Graph(id=f'fig_tezgah_{costcenter}_{interval}_{position}')
                            ),
                        ],
                        className="grafik",
                    ),
                    className="col-lg-5 col-md-6 col-sm-12",
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.Div(
                                    className="row text-center text-light",
                                    children=[
                                        dbc.Col(html.H3("Genel Personel Verimliliği"),
                                                className="bg-primary col-lg-7 ic-yazilar"),
                                        dbc.Col([
                                            html.H3(id=f'performance_{costcenter}_{interval}_{position}'),
                                            html.P("Hedef %90")
                                        ], className="bg-warning col-lg-5 ic-yazilar-2 p-2")
                                    ]
                                )
                            ),
                            dbc.CardBody(
                                dcc.Graph(id=f'fig_personal_{costcenter}_{interval}_{position}')
                            ),
                        ],
                        className="grafik",
                    ),
                    className="col-lg-5 col-md-6 col-sm-12",
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.Div(
                                    className="row text-center text-light",
                                    children=[
                                        dbc.Col(html.H3("Genel OEE Verimliliği"),
                                                className="bg-primary col-lg-7 ic-yazilar"),
                                        dbc.Col([
                                            html.H3(id=f'oee_{costcenter}_{interval}_{position}'),
                                            html.P("Hedef %65")
                                        ], className="bg-warning col-lg-5 ic-yazilar-2 p-2")
                                    ]
                                )
                            ),
                            dbc.CardBody(
                                dcc.Graph(id=f'fig_oee_{costcenter}_{interval}_{position}')
                            ),
                        ],
                        className="grafik",
                    ),
                    className="col-lg-5 col-md-6 col-sm-12",
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.Div(
                                    className="row text-center text-light",
                                    children=[
                                        dbc.Col(html.H3("Genel Kapasite Verimliliği"),
                                                className="bg-primary col-lg-7 ic-yazilar"),
                                        dbc.Col([
                                            html.H3("nan"),
                                            html.P("nan")
                                        ], className="bg-warning col-lg-5 ic-yazilar-2 p-2")
                                    ]
                                )
                            ),
                            dbc.CardBody(
                                dcc.Graph(id=f'fig_kapasite_{costcenter}_{interval}_{position}')
                            ),
                        ],
                        className="grafik",
                    ),
                    className="col-lg-5 col-md-6 col-sm-12",
                ),
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                dbc.Card([
                                    dbc.CardHeader(html.H5("Planlı Duruş (Set-up)", className="card-title")),
                                    dbc.CardBody([
                                        dcc.Graph(id=f"fig_planlı_{costcenter}_{interval}_{position}", style={"height": "400px"})
                                    ])
                                ], className="grafik-divler")
                            ], className="mt-4")
                        ], lg=3, md=3, sm=12),

                        dbc.Col([
                            html.Div([
                                dbc.Card([
                                    dbc.CardHeader(html.H5("Plansız Duruş", className="card-title")),
                                    dbc.CardBody([
                                        dcc.Graph(id=f"fig_plansız_{costcenter}_{interval}_{position}", style={"height": "400px"})
                                    ])
                                ], className="grafik-divler mt-4")
                            ])
                        ], lg=3, md=3, sm=12),

                        dbc.Col([
                            html.Div([
                                dbc.Card([
                                    dbc.CardHeader(html.H5("Kalite Duruşları", className="card-title")),
                                    dbc.CardBody([
                                        dcc.Graph(id=f"fig_kalite_{costcenter}_{interval}_{position}", style={"height": "400px"})
                                    ])
                                ], className="grafik-divler mt-4")
                            ])
                        ], lg=3, md=3, sm=12)
                    ], className="justify-content-center aligns-item-center d-flex")
                ])
            ], style={"margin-left": "20px", "margin-bottom": "50px"},
        )] ),
        dbc.Row(html.H5("Performans(( Kullanılabilirlik(( OEE", style={
            "background-color": "#2149b4",
            "text-align": "center",
            "color": "white",
            "padding": 6,
        })),
        dbc.Row(
            dbc.Col(html.Div(id=f'sunburst_forreports_{costcenter}_{interval}_{position}'),
                    width=12, className="d-flex justify-content-center", )
            , className="g-0"),
        dbc.Row([
            dbc.Col(children=[
                dbc.Row(html.H5("Üretim Özeti", style={
                    "background-color": "#2149b4",
                    "text-align": "center",
                    "color": "white",
                    "padding": 6,
                })),
                dbc.Row([
                    dbc.Col([
                        dbc.Col(id=f"my-output_forreports_{costcenter}_{interval}_{position}", width={"size": 2},
                                style={"margin-left": 0}),
                        dbc.Col([return_sparks(graph1=f"fig_prod_{costcenter}_{interval}_{position}",
                                               graph2=f"fig_working_machine_{costcenter}_{interval}_{position}",
                                               margin_left=0)],
                                width={"size": 2}),
                        dbc.Col(id=f"my-output_forreports_{costcenter}2_{interval}_{position}", width={"size": 2},
                                style={"margin-left": 0}),
                        dbc.Col([return_sparks(graph1=f"fig_ppm_{costcenter}_{interval}_{position}",
                                               graph2=f"fig_scrap_{costcenter}_{interval}_{position}",
                                               margin_left=0)],
                                width={"size": 2})], className="d-flex justify-content-center", width=12)
                ], className="g-0")
            ], style={})
        ]),
        dbc.Row([
            dbc.Col(children=[

                dbc.Row(html.H5("Üretim Zaman Çizgisi", style={
                    "background-color": "#2149b4",
                    "text-align": "center",
                    "color": "white",
                    "padding": 6,
                    "margin-bottom": "60px",
                })),
                dbc.Row(
                    dbc.Col([
                        html.Div(id=f'gann_forreports_{costcenter}_{interval}_{position}')],
                        className="d-flex justify-content-center", width=12)
                    , className="g-0")],
                style={"margin-bottom": "30px"}, width={"size": 12}
            ), ]),
        dbc.Row([
            dbc.Col(children=[

                dbc.Row(html.H5("Üretim Duruşları", style={
                    "background-color": "#2149b4",
                    "text-align": "center",
                    "color": "white",
                    "padding": 6,
                    "margin-bottom": "60px",
                })),
                dbc.Row(
                    dbc.Col([
                        html.Div(id=f'bubble_forreports_{costcenter}_{interval}_{position}')],
                        className="d-flex justify-content-center", width=12)
                    , className="g-0")],
                style={"margin-bottom": "60px", }, width={"size": 12}
            ), ]),
        dbc.Row([
            dbc.Col(children=[

                html.H5("Hurda ve Nedenleri", style={
                    "height": 25,
                    "text-align": "center",
                    "background-color": "#2149b4",
                    "color": "white",
                    "margin-top": "50px",
                    "padding": 6,
                    "margin-bottom": "60px",
                }),
                dbc.Row(
                    dbc.Col([
                        html.Div(id=f'fig_scatscrap_forreports_{costcenter}_{interval}_{position}')],
                        className="d-flex justify-content-center", width=12)
                    , className="g-0")],
                style={"margin-bottom": "60px", }, width={"size": 12}
            ), ])
        ,
        html.Div(id=f"generated_1graph1data_for_report_{costcenter}_{interval}_{position}")]

        , style={"justify-content": "center", "align-items": "center"}, fluid=True)


def return_sparks(graph1="fig_prod_forreports", graph2="fig_scrap_forreports", margin_left=0):
    return html.Div(children=[dcc.Graph(id=graph1, figure={},
                                        style={'width': '4vh', 'height': '2vh', "margin-top": 50,
                                               "margin-left": margin_left}),
                              dcc.Graph(id=graph2, figure={},
                                        style={'width': '4vh', 'height': '2vh', "margin-top": 100,
                                               "margin-left": margin_left})])


def return_adr_callbacks(costcenter='cnc', interval='day',position = '475px'):
    if interval in ['week' , 'month']:
        @app.callback(
            [Output(f'fig_oee_{costcenter}_{interval}_{position}', 'figure'),
             Output(f'fig_personal_{costcenter}_{interval}_{position}', 'figure'),
             Output(f'fig_tezgah_{costcenter}_{interval}_{position}', 'figure'),
             Output(f'fig_planlı_{costcenter}_{interval}_{position}', 'figure'),
             Output(f'fig_plansız_{costcenter}_{interval}_{position}', 'figure'),
             Output(f'fig_kalite_{costcenter}_{interval}_{position}', 'figure'),
             Output(f'availability_{costcenter}_{interval}_{position}', 'children'),
             Output(f'performance_{costcenter}_{interval}_{position}', 'children'),
             Output(f'oee_{costcenter}_{interval}_{position}', 'children')
             ],
            Input(component_id=f'work-dates_{costcenter}_{interval}_{position}', component_property='data')
        )
        def historical_values(dates):
            work_date = datetime.strptime(dates["workend"], '%Y-%m-%d')
            day_of_week = work_date.weekday()

            df_oees = ag.run_query(f"SELECT TOP 7 * FROM VLFOEE WHERE PERIOD = '{interval}' AND COSTCENTER = '{costcenter}'"
                                   f" AND OEEDATE <= '{dates['workend']}' ORDER BY OEEDATE DESC")

            df_downs = ag.run_query(
                f"EXEC VLFPROCPRDFOROEE '{dates['workstart']}','{dates['workend']}','{interval}', '{costcenter.upper()}'")

            if costcenter == 'cnc':
                df_downs = df_downs[df_downs["COSTCENTER"] == 'CNC']
            elif costcenter == 'preshane1':
                df_downs = df_downs[df_downs["COSTCENTER"] == costcenter.upper()]
            elif costcenter == 'preshane2':
                df_downs = df_downs[df_downs["COSTCENTER"] == costcenter.upper()]


            fig = px.line(df_oees, x="OEEDATE", y="OEE")
            fig_personal = px.line(df_oees, x="OEEDATE", y="PERFORMANCE")
            fig_tezgah = px.line(df_oees, x="OEEDATE", y="AVAILABILITY")

            fig_planlı = px.line(df_downs, x="WORKEND", y="SETUP").update_layout(margin=dict(l=0, r=0, t=0, b=0))
            fig_plansız = px.line(df_downs, x="WORKEND", y="PLANSIZ").update_layout(margin=dict(l=0, r=0, t=0, b=0))
            fig_kalite = px.line(df_downs, x="WORKEND", y="KALITE").update_layout(margin=dict(l=0, r=0, t=0, b=0))

            return [fig, fig_personal, fig_tezgah, fig_planlı, fig_plansız, fig_kalite,
                    df_oees["AVAILABILITY"][0], df_oees["PERFORMANCE"][0], df_oees["OEE"][0]]

    @app.callback(
        Output(f'valid_data_{costcenter}_{interval}_{position}', 'children'),
        [Input(component_id=f'oeeelist5_{costcenter}_{interval}_{position}', component_property='data')]
    )
    def update_data(oeelist6):
        oeelist6=json.loads(oeelist6)
        oeelist6 = pd.DataFrame(oeelist6['data'], columns=oeelist6['columns'])

        print(oeelist6)
        print("*********")

        oeelist6 = oeelist6[oeelist6["COSTCENTER"] == costcenter.upper()]
        # Filtering data based on BADDATA_FLAG
        data1 = oeelist6[oeelist6['BADDATA_FLAG'] == 0]
        data1['SUMS'].iloc[-1]

        # Alternatively, if you need the value at a specific dynamic index, say stored in a variable 'index':
        index = data1['SUMS'].index[-1]  # This sets 'index' to the last index dynamically
        value = data1['SUMS'][index]
        data2 = oeelist6[oeelist6['BADDATA_FLAG'] != 0]['SUMS'].sum()

        print("*****")
        print(data2)
        print("*****")

        # Preparing the text for output
        text = f"{costcenter}  {data1['SUMS'].iloc[-1]} adet geçerli ve  {data2} adet geçersiz data noktasına sahip."
        return text

    @app.callback(
        [Output(component_id=f'my-output_forreports_{costcenter}_{interval}_{position}', component_property='children'),
         Output(component_id=f'my-output_forreports_{costcenter}2_{interval}_{position}', component_property='children')],
        [Input(component_id=f'work-dates_{costcenter}_{interval}_{position}', component_property='data'),
         Input(component_id=f'oeeelist6_{costcenter}_{interval}_{position}', component_property='data')]
    )
    def return_summary_data(dates, oeeelist6):
        print("summary running")
        oeeelist6 = pd.read_json(oeeelist6, orient='split')
        df_working_machines = ag.run_query(query=r"EXEC VLFWORKINGWORKCENTERS @WORKSTART=?, @WORKEND=?, @INTERVAL=?"
                                           , params=(dates["workstart"], dates["workend"],interval))
        data1 = ["Production Volume", get_daily_qty(df=oeeelist6, costcenter=costcenter.upper())]
        data2 = ["Working Machines",
                 working_machinesf(working_machines=df_working_machines, costcenter=costcenter.upper())[-1]]
        data3 = ["PPM", get_daily_qty(df=oeeelist6, costcenter=costcenter.upper(), ppm=True)]
        data4 = ["Scrap", get_daily_qty(df=oeeelist6, costcenter=costcenter.upper(), type='HURDA')]

        return [html.Div(children=[html.Div(children=data1[1],
                                            style={"fontSize": 30, "color": summary_color,
                                                   'text-align': 'center'}),
                                   html.Div(children=data1[0],
                                            style={"fontSize": 12, "color": summary_color,
                                                   'text-align': 'center'}),
                                   html.Br(),
                                   html.Div(children=data2[1],
                                            style={"fontSize": 30, "color": summary_color,
                                                   'text-align': 'center', "margin-top": 20}),
                                   html.Div(children=data2[0],
                                            style={"fontSize": 12, "color": summary_color,
                                                   'text-align': 'center'}),
                                   ],
                         style={"width": 300, "height": 250, 'color': px.colors.qualitative.Set3[1],
                                'fontSize': 25, 'text-align': 'left', "margin-top": 65, "margin-left": 0
                                }),
                html.Div(children=[html.Div(children=data3[1],
                                            style={"fontSize": 30, "color": summary_color,
                                                   'text-align': 'center'}),
                                   html.Div(children=data3[0],
                                            style={"fontSize": 12, "color": summary_color,
                                                   'text-align': 'center'}),
                                   html.Br(),
                                   html.Div(children=data4[1],
                                            style={"fontSize": 30, "color": summary_color,
                                                   'text-align': 'center', "margin-top": 20}),
                                   html.Div(children=data4[0],
                                            style={"fontSize": 12, "color": summary_color,
                                                   'text-align': 'center'}),
                                   ],
                         style={"width": 300, "height": 250, 'color': px.colors.qualitative.Set3[1],
                                'fontSize': 25, 'text-align': 'left', "margin-top": 65, "margin-left": 0
                                })]

    # ------------------------------------------------------------------------------

    @app.callback(
        Output(component_id=f'sunburst_forreports_{costcenter}_{interval}_{position}', component_property='children'),
        Input(component_id=f'oeeelist0_{costcenter}_{interval}_{position}', component_property='data')
    )
    def update_graph_sunburst_forreports_(oeeelist0):
        print("pie running")
        return return_piechart(costcenter.upper(), oeeelist0, 1)

    @app.callback(
        Output(component_id=f'bubble_forreports_{costcenter}_{interval}_{position}', component_property='children'),
        Input(component_id=f'oeeelist2_{costcenter}_{interval}_{position}', component_property='data'))
    def update_graph_bubble_forreports_(oeeelist2):
        graphwidth = 950
        oeeelist2 = pd.read_json(oeeelist2, orient='split')
        df, category_order = scatter_plot(df=oeeelist2.loc[oeeelist2["COSTCENTER"] == costcenter.upper()])

        # Generate a dynamic color map by assigning colors from Alphabet to each unique 'STEXT' value
        color_map = {category: color for category, color in zip(category_order, px.colors.qualitative.Alphabet)}

        figs = px.histogram(df, x="WORKCENTER", y="FAILURETIME",
                            color="STEXT",
                            hover_data=["WORKCENTER"],
                            color_discrete_map=color_map, category_orders={"STEXT": category_order})
        # figs.update_traces(textfont=dict(family=['Arial Black']))
        figs.update_xaxes(type="category", tickangle=90, fixedrange=True, categoryorder='total ascending'
                          , tickfont=dict(
                color='black',  # Set tick label color to white
                size=13,  # Set font size (adjust as needed)
                family='Arial Black')
                          ),

        # figs.update_yaxes(categoryorder="total descending")
        figs.update_layout(margin=dict(l=100, r=70, t=100, b=100),
                           barmode='overlay',
                           xaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)'),
                           yaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)'),
                           paper_bgcolor=layout_color, plot_bgcolor=layout_color, font_color=summary_color,
                           title_font_family="Times New Roman", title_font_color="red", width=graphwidth, height=500,
                           showlegend=False,
                           xaxis_title="",
                           yaxis_title=""
                           )

        return html.Div(
            [dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=figs), width=10), dbc.Col(legend_generater(color_map, 10), width=2)])])

    @app.callback(
        Output(component_id=f'gann_forreports_{costcenter}_{interval}_{position}', component_property='children'),
        Input(component_id=f'oeeelist2_{costcenter}_{interval}_{position}', component_property='data')
    )
    def update_chart_gann_forreports_(oeeelist2):
        graphwidth = 900
        color_map = {"Uretim": "forestgreen", "Plansiz Durus": "red"
            , "Ariza Durusu": "Brown", "Planli Durus": "Coral"
            , "Kurulum": "Aqua"}
        oeeelist2 = pd.read_json(oeeelist2, orient='split')
        df = oeeelist2.loc[oeeelist2["COSTCENTER"] == costcenter.upper()]
        df.sort_values(by="CONFTYPE", ascending=False, inplace=True)
        figs = px.timeline(data_frame=df[["WORKSTART", "WORKEND", "WORKCENTER", "CONFTYPE", "STEXT", "QTY"]],
                           x_start="WORKSTART",
                           x_end="WORKEND",
                           y='WORKCENTER', color="CONFTYPE",
                           color_discrete_map=color_map)

        figs.update_xaxes(type="date", tickangle=90, fixedrange=True, tickfont=dict(
            color='grey',  # Set tick label color to white
            size=13,  # Set font size (adjust as needed)
            family='Arial Black')),

        figs.update_yaxes(categoryorder="category ascending", tickfont=dict(
            color='black',  # Set tick label color to white
            size=13,  # Set font size (adjust as needed)
            family='Arial Black'))
        figs.update_layout(margin=dict(l=100, r=70, t=100, b=100), barmode='overlay', paper_bgcolor=layout_color,
                           plot_bgcolor='rgba(0, 0, 0, 0)',
                           font_color=summary_color,
                           title_font_family="Times New Roman", title_font_color="red", width=graphwidth, height=800,
                           showlegend=False,
                           xaxis_title="",
                           yaxis_title=""
                           )

        return html.Div(
            [dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=figs), width=10), dbc.Col(legend_generater(color_map, margin_left=20), width=2)])])
        # dcc.Graph(figure=legend_generater(color_map)),

    def get_spark_line(data=pd.DataFrame(), range=list(range(24))):
        return go.Figure(

            {
                "data": [
                    {
                        "x": range,
                        "y": data,
                        "mode": "lines+markers",
                        "name": "item",
                        "line": {"color": summary_color},
                    }
                ],
                "layout": {
                    "margin": dict(l=50, r=0, t=4, b=4, pad=0),
                    "uirevision": True,
                    "xaxis": dict(
                        showline=False,
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False,
                    ),
                    "yaxis": dict(
                        showline=False,
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False,
                    ),
                    "paper_bgcolor": layout_color,
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "width": 300,
                    "height": 65
                },
            }
        )

    @app.callback(
        [Output(component_id=f'fig_prod_{costcenter}_{interval}_{position}', component_property='figure'),
         Output(component_id=f'fig_scrap_{costcenter}_{interval}_{position}', component_property='figure'),
         Output(component_id=f'fig_working_machine_{costcenter}_{interval}_{position}', component_property='figure'),
         Output(component_id=f'fig_ppm_{costcenter}_{interval}_{position}', component_property='figure')],
        Input(component_id=f'work-dates_{costcenter}_{interval}_{position}', component_property='data'),
        Input(component_id=f'oeeelist6_{costcenter}_{interval}_{position}', component_property='data')
    )
    def update_spark_line(dates, oeeelist6):
        onemonth_prdqty = pd.read_json(oeeelist6, orient='split')
        df_working_machines = ag.run_query(query=r"EXEC VLFWORKINGWORKCENTERS @WORKSTART=?, @WORKEND=?, @INTERVAL=?"
                                           , params=(dates["workstart"], dates["workend"],interval))
        fig_prod_forreports = get_spark_line(
            data=generate_for_sparkline(data=onemonth_prdqty, proses=costcenter.upper()))
        fig_scrap__forreports = get_spark_line(
            data=generate_for_sparkline(data=onemonth_prdqty, proses=costcenter.upper(), type='HURDA'))
        fig_working_machine_forreports = get_spark_line(
            data=working_machinesf(working_machines=df_working_machines))
        fig_ppm_forreports = get_spark_line(
            data=generate_for_sparkline(data=onemonth_prdqty, proses=costcenter.upper(), ppm=True))
        return [fig_prod_forreports, fig_scrap__forreports, fig_working_machine_forreports, fig_ppm_forreports]

    @app.callback(
        Output(component_id=f'fig_scatscrap_forreports_{costcenter}_{interval}_{position}', component_property='children'),
        Input(component_id=f'work-dates_{costcenter}_{interval}_{position}', component_property='data')
    )
    def create_scatterplot_for_scrapqty(dates):
        graphwidth = 900
        df_scrap = ag.run_query(query=r"EXEC VLFPRDSCRAPWITHPARAMS @WORKSTART=?, @WORKEND=?"
                                , params=(dates["workstart"], dates["workend"]))

        df_scrap = df_scrap[df_scrap["COSTCENTER"].str.contains(costcenter.upper(), na=False)]

        cat_order_sumscrap = df_scrap.groupby("STEXT")["SCRAP"].sum().sort_values(ascending=False).index
        df_scrap["SCRAP"] = df_scrap["SCRAP"].astype("int")
        category_order = df_scrap["STEXT"].unique()
        color_map = {category: color for category, color in zip(category_order, px.colors.qualitative.Alphabet)}

        fig = px.histogram(data_frame=df_scrap,
                           x="WORKCENTER",
                           y="SCRAP",
                           color="STEXT",
                           color_discrete_map=color_map,
                           hover_data=["MTEXTX"],
                           width=1500, height=500,
                           histfunc='sum',
                           category_orders={"STEXT": cat_order_sumscrap})

        # fig.update_traces(textfont=dict(family=['Arial Black']))
        fig.update_xaxes(type="category", tickangle=90, fixedrange=True, tickfont=dict(
            color='grey',  # Set tick label color to white
            size=13,  # Set font size (adjust as needed)
            family='Arial Black')),  # figs.update_yaxes(categoryorder="total descending")
        fig.update_layout(margin=dict(l=100, r=70, t=100, b=100), barmode='relative', paper_bgcolor=layout_color,
                          plot_bgcolor='rgba(0, 0, 0, 0)',
                          font_color=summary_color,
                          title_font_family="Times New Roman", title_font_color="red", width=graphwidth, height=400,
                          showlegend=False,
                          xaxis_title="",
                          yaxis_title=""
                          )
        return html.Div([dbc.Row([dbc.Col(dcc.Graph(figure=fig), width=10),
                                  dbc.Col(legend_generater(color_map, 12), width=2, style={'margin-left': 0})])])

    @app.callback(
        [Output(f"generated_1graph1data_for_report_{costcenter}_{interval}_{position}", "children")],
        [Input(f"work-dates_{costcenter}_{interval}_{position}", "data"),
         Input(component_id=f'oeeelist1_{costcenter}_{interval}_{position}', component_property='data'),
         Input(component_id=f'oeeelist3_{costcenter}_{interval}_{position}', component_property='data'),
         Input(component_id=f'oeeelist7_{costcenter}_{interval}_{position}', component_property='data')])
    def update_ind_fig(params, oeeelist1w, oeeelist3w, oeeelist7w):
        """
        Callback to update individual figures for each work center in the selected cost center.

        Args:
            list_of_wcs (list): The list of work centers to display.
            option_slctd = costcenter.upper() (str): The selected cost center.
            report_day (str): The date for which to display the report. Default is "2022-07-26".

        Returns:
            tuple: A tuple containing lists of figures, data, columns, and styles for each work center.

        Parameters
        ----------
        oeeelist7w
        oeeelist3w
        params
        report_type
        option_slctd = costcenter.upper()
        oeeelist1w
        """

        params["interval"] = 'day'

        def return_layout(report_type='wc'):
            list_of_figs, list_of_data, list_of_columns, list_of_styles = workcenters(costcenter.upper(), report_type,
                                                                                      params,
                                                                                      oeeelist1w, oeeelist3w,
                                                                                      oeeelist7w)

            def create_column(fig, data, columns, margin_left):
                return dbc.Col(
                    [dbc.Row(
                        dcc.Graph(figure=fig, style={'margin-left': 200,'position':'relative', 'bottom':position,})),
                        dbc.Row(
                            dash_table.DataTable(
                                data=data,
                                columns=columns,
                                style_cell={
                                    'color': 'black',
                                    'backgroundColor': 'rgba(255, 255, 255, 0.8)',
                                    'minWidth': '20px', 'width': '80px', 'maxWidth': '60px',
                                    'textAlign': 'center',
                                    'border': '1px solid black',
                                    'minWidth': '80px', 'maxWidth': '300px',
                                    'fontSize': '12px',
                                },
                                style_table={
                                    'height': '150px',
                                    'width': '800px',
                                    'overflowY': 'auto',
                                    'borderCollapse': 'collapse',
                                    'border': '1px solid black',
                                    'margin-left': 13,
                                },
                                style_header={
                                    'fontWeight': 'bold',
                                    'backgroundColor': 'rgba(0, 0, 0, 0.1)',
                                    'borderBottom': '1px solid black',
                                    'color': 'black',
                                },
                                style_data_conditional=[]
                            ), style={'margin-top': 7})
                    ],
                    width=4,
                    style={'margin-left': 45, "justify-content": "center", "align-items": "center",
                           "height": "700px", "width": "850px",
                           "background-color": "rgba(255, 255, 255, 0.314)","margin-top": 50, "border-radius": "10px"}
                )

            # This list comprehension creates all columns needed for the layout
            columns = [create_column(list_of_figs[i], list_of_data[i], list_of_columns[i], 0 if i % 2 == 0 else 300) for
                       i
                       in range(len(list_of_figs))]

            # This code groups the columns into rows of 3 columns each
            rows = [dbc.Row(columns[i:i + 1], style={"margin-bot": 0}) for i in range(2, len(columns), 1)]

            layout = html.Div(children=rows, style={"margin-bot": 0})
            return layout

        return [html.Div([
            dbc.Row([
                dbc.Col([
                    html.H5("İş Merkezi Göstergeleri", style={
                        "background-color": "#2149b4",
                        "text-align": "center",
                        "color": "white",
                    }), return_layout("wc")], style={"border": "5px solid black","background-color":"gray"},),
                dbc.Col([
                    html.H5("Personel Göstergeleri", style={
                        "background-color": "#2149b4",
                        "text-align": "center",
                        "color": "cyan",
                        "border-left": "5px solid black",
                    }), return_layout("pers")], style={"border": "5px solid black","background-color":"gray"},),])
        ])]


def return_adr_timecallbacks(costcenter, interval='day',position= '200px'):
    @app.callback(
        Output(f'interval-trigger_{costcenter}_{interval}_{position}', 'max_intervals'),
        Input(f'check-interval_{costcenter}_{interval}_{position}', 'n_intervals'),
        State(f'trigger-timestamp_{costcenter}_{interval}_{position}', 'data')
    )
    def check_elapsed_time(_, trigger_timestamp):
        if trigger_timestamp is None:
            # If there's no timestamp, it means the initial trigger hasn't happened yet
            return no_update

        current_time = datetime.now().timestamp()
        elapsed_time = current_time - trigger_timestamp

        if elapsed_time >= 600:  # 600 seconds = 10 minutes
            return no_update  # Or set to a specific number if you want to limit future triggers

        return no_update

    @app.callback(
        Output(f'trigger-timestamp_{costcenter}_{interval}_{position}', 'data'),
        Input(f'interval-trigger_{costcenter}_{interval}_{position}', 'n_intervals')
    )
    def set_trigger_timestamp(n):
        if n == 1:  # Triggered once
            return datetime.now().timestamp()
        else:
            raise PreventUpdate

    @app.callback(
        [
            Output(f'oeeelist0_{costcenter}_{interval}_{position}', 'data'),
            Output(f'oeeelist1_{costcenter}_{interval}_{position}', 'data'),
            Output(f'oeeelist2_{costcenter}_{interval}_{position}', 'data'),
            Output(f'oeeelist3_{costcenter}_{interval}_{position}', 'data'),
            Output(f'oeeelist5_{costcenter}_{interval}_{position}', 'data'),
            Output(f'oeeelist6_{costcenter}_{interval}_{position}', 'data'),
            Output(f'oeeelist7_{costcenter}_{interval}_{position}', 'data'),
            Output(f'work-dates_{costcenter}_{interval}_{position}', 'data'),
        ],
        [Input(f'interval-trigger_{costcenter}_{interval}_{position}', 'n_intervals')]
    )
    def update_data_on_page_load(pathname):
        # If there's no specific action tied to pathname, you could check for it here
        # For now, we assume every load/refresh should trigger the data update
        print(pathname)
        print(" main here")
        if not pathname:
            print(" prevent here")


            raise PreventUpdate

        print("running")

        if interval == 'day':
            print("***********")
            print(f"kb is {kb} and date is {date.today() - timedelta(days=kb)}")
            print("***********")
            data_points = prdconf(((date.today() - timedelta(days=kb)).isoformat(),
                                   (date.today() - timedelta(days=kb - 1)).isoformat(), interval))
            # Prepare the data for each store
            data_for_stores = [data_points[i] for i in range(len(data_points)) if i in [0, 1, 2, 3, 5,6, 7]]
            work_dates_data = {"workstart": (date.today() - timedelta(days=kb)).isoformat(),
                               "workend": (date.today() - timedelta(days=kb - 1)).isoformat()}
        elif interval == 'week':

            #Bir önceki haftanın başlangıç ve bitiş günlerini getirir.

            current_date = datetime.now().date()
            if current_date.weekday() in (0,1,2,3):
                first_day = current_date - (timedelta(days=current_date.weekday() + 7))
                last_day =  current_date +(timedelta(days=current_date.weekday()-1))
            else:
                first_day = current_date + (timedelta(days=current_date.weekday() ))
                last_day =  first_day + timedelta(days=7)

            print(f"***************!!!!!!! {first_day} - {last_day} Tarihleri Arası Haftalık Rapor Verileri Çekiliyor.***************!!!!!!!")
            # Assuming kb is defined and prdconf is your data-fetching function
            data_points = prdconf((first_day.isoformat(),
                                   last_day.isoformat(), interval))


            # Prepare the data for each store
            data_for_stores = [data_points[i] for i in range(len(data_points)) if i in [0, 1, 2, 3,5, 6, 7]]
            work_dates_data = {"workstart": first_day.isoformat(),
                               "workend": last_day.isoformat()}

        else:

            #Bir önceki haftanın başlangıç ve bitiş günlerini getirir.

            current_date = datetime.now().date()


            if current_date.day <= 17:
                # Get the first and last day of the previous month
                first_day = current_date.replace(day=1) - timedelta(days=1)
                first_day = first_day.replace(day=1)
                last_day = current_date.replace(day=1) - timedelta(days=1)
            else:
                # Get the first and last day of the current month
                first_day = current_date.replace(day=1)
                last_day = current_date.replace(day=1) + timedelta(days=31)
                last_day = last_day.replace(day=1) - timedelta(days=1)

            print(
                f"***************!!!!!!! {first_day} - {last_day} Tarihleri Arası {interval} Rapor Verileri Çekiliyor.***************!!!!!!!")
            # Assuming kb is defined and prdconf is your data-fetching function
            data_points = prdconf((first_day.isoformat(), last_day.isoformat(), interval))

            # Prepare the data for each store
            data_for_stores = [data_points[i] for i in range(len(data_points)) if i in [0, 1, 2, 3,5, 6, 7]]
            work_dates_data = {"workstart": first_day.isoformat(), "workend": last_day.isoformat()}

        # Return the data for each store
        print("********")
        return *data_for_stores, work_dates_data
    # Connect the Plotly graphs with Dash Components
