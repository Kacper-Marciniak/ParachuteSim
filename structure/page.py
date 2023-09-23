from dash import dcc, html
import dash_bootstrap_components as dbc
from structure.plotter import getEmptyPlot

def serveNavbar():
    navbar = dbc.Navbar([
        html.Div([
            html.Div(
                [
                    html.A(html.Img(src=r"assets\logo.png", height="50px", style={"padding": "5px"}), href=r'https://pwrinspace.pwr.edu.pl/'),
                ], style={
                        "display": "flex",
                        "justify-content": "left",
                        "align-items": "center",
                        "margin-left": "10px"
                    }
                ),
            html.H1("ParaSim", className="app-title"),


        ], style={
                "display": "grid",
                "grid-template-columns": "1fr auto 1fr",
                "width": "100%",
                "height": "100%",
                "justify-content": "space-between",
                "align-items": "center"
            }
        )
    ], style={
            "background-color": "white",
            "width": "100%",
            "height": "75px",
            "box-shadow": "0px 0px 15px rgba(50,50,50,0.25)",
        },
        sticky='top'
    )
    return navbar

def serveBody():
    return html.Div(
            [                
                html.H2(
                    "Wymagana średnica czaszy spadochronu",
                    style = {
                        "background-color": "rgba(50,50,50,0.1)",
                        "padding": "10px",
                        "border-radius": "10px",
                        "width": "100%",
                        'grid-row': '1',
                        'grid-column': '1/-1',
                    }),
                dbc.Card([
                    dbc.CardHeader("Parametry wejściowe"), 
                    dbc.CardBody([
                        html.Div(
                        [
                            "Masa pojazdu [kg]:",
                            dcc.Input(type='number', id='simulation1-mass-input', min=0, step=.1, value=5.0),
                            "Zakres prędkości opadania: min [m/s]:",
                            dcc.Input(type='number', id='simulation1-velocitystart-input', min=0, step=.5, value=5.0),
                            "Zakres prędkości opadania: max [m/s]:",
                            dcc.Input(type='number', id='simulation1-velocitystop-input', min=0, step=.5, value=25.0),
                            "Oczekiwana prędkość opadania [m/s]:",
                            dcc.Input(type='number', id='simulation1-velocity-input', min=0, step=1, value=10.0),
                        ], style={
                            "display": "grid",
                            "grid-template-columns": "auto 1fr",
                            "width": "100%",
                            "gap": "5px",
                            "text-align": "right",
                            "padding": "5px"
                        }
                        )
                    ]),
                ], style={
                    'grid-row': '2',
                    'grid-column': '1',
                    'height': '100%'
                }),
                dbc.Button(
                    "Przelicz",
                    id="simulation1-run-button",
                    style = {
                        'width': '100%',
                        'margin': '5px',
                        'background-color': '#00c896',
                        'color': 'white',
                        'border-color': '#00c896'
                    }
                ), 
                dbc.Card([
                    dbc.CardHeader("Wyniki"), 
                    dbc.CardBody([
                        html.Div(
                            [
                                dcc.Graph(
                                    id = 'simulation1-results-plot',
                                    figure = getEmptyPlot(),
                                    config = {'responsive': False, "displayModeBar": False},
                                    style={"width": "100%", "height": "100%"},
                                ),
                            ], style={
                                "width": "100%",
                                "height": "100%",
                                "padding" : "5px"
                            }
                        )
                    ]),
                ], style={
                    'grid-row': '2/4',
                    'grid-column': '2',
                    'height': '100%'
                }),               
                html.H2(
                    "Obciążenia przy otwarciu spadochronu",
                    style = {
                        "background-color": "rgba(50,50,50,0.1)",
                        "padding": "10px",
                        "border-radius": "10px",
                        "width": "100%",
                        'grid-row': '4',
                        'grid-column': '1/-1',
                    }),
                dbc.Card([
                    dbc.CardHeader("Parametry wejściowe"), 
                    dbc.CardBody([
                        html.Div(
                        [
                            "Masa pojazdu [kg]:",
                            dcc.Input(type='number', id='simulation2-mass-input', min=0, step=.1, value=5.0),
                            html.Div([]), 
                            "Oczekiwana prędkość opadania [m/s]:",
                            dcc.Input(type='number', id='simulation2-velocity-input', min=0, step=.1, value=10.0),
                            dcc.Checklist(
                                id = 'simulation2-velocity-checkmark',
                                options = [{'label':'', 'value':'use'}],
                                value = ['use'],
                                persistence = True,
                                persistence_type = 'session',
                                style={
                                    "width": "auto",
                                }
                            ),
                            "Średnica spadochronu [m]:",
                            dcc.Input(type='number', id='simulation2-diameter-input', min=0, step=.05, value=0.30),
                            dcc.Checklist(
                                id = 'simulation2-diameter-checkmark',
                                options = [{'label':'', 'value':'use'}],
                                value = [],
                                persistence = True,
                                persistence_type = 'session',
                                style={
                                    "width": "auto",
                                }
                            ),
                        ], style={
                            "display": "grid",
                            "grid-template-columns": "auto 1fr auto",
                            "width": "100%",
                            "gap": "5px",
                            "text-align": "right",
                            "padding": "5px"
                        }
                        )
                    ]),
                ], style={
                    'grid-row': '5',
                    'grid-column': '1',
                    'height': '100%'
                }),
                dbc.Button(
                    "Przelicz",
                    id="simulation2-run-button",
                    style = {
                        'width': '100%',
                        'margin': '5px',
                        'background-color': '#00c896',
                        'color': 'white',
                        'border-color': '#00c896'
                    }
                ), 
                dbc.Card([
                    dbc.CardHeader("Wyniki"), 
                    dbc.CardBody([
                        html.Div(
                            id = "simulation2-numericdata-container",
                            style={
                                
                                "width": "100%",
                                "padding": "5px",
                                "gap": "5px"
                            }                    
                        )
                    ]),
                ], style={
                    'grid-row': '5/-1',
                    'grid-column': '2',
                    'height': '100%'
                }),
            ],
            style = {
                "display": "grid",
                "grid-template-columns": "600px 1fr",
                "grid-template-rows": "auto 1fr auto auto 1fr auto",
                "gap": "10px",
                "align-items": "stretch",
                "justify-content": "space-between",   
                "width": "100%",    
            }
        )
