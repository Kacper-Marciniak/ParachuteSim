from dash import dcc, html
import dash_bootstrap_components as dbc
from structure.plotter import getEmptyPlot
from calculations.ConstantParameters import *

BASE_COLOR = '#008ede'

def serveNavbar():
    navbar = dbc.Navbar([
        html.Div([
            html.Div(
                [
                    html.A(html.Img(src=r"assets\logo_pwr.png", height="50px"), href=r'https://pwr.edu.pl/', className='logo-navbar'),
                    html.A(html.Img(src=r"assets\logo2.png", height="50px"), href=r'https://pwrinspace.pwr.edu.pl/', className='logo-navbar'),
                ], style={
                        "display": "flex",
                        "justify-content": "left",
                        "align-items": "center",
                        "margin-left": "10px",
                        "gap": "5px",
                    }
                ),
            html.H1("ParaSim", style={"color": BASE_COLOR}),


        ], style={
                "display": "grid",
                "grid-template-columns": "1fr auto 1fr",
                "width": "100%",
                "height": "100%",
                "justify-content": "space-between",
                "align-items": "center"
            }
        )
    ], 
    className= 'card-footer',
    style={'height': '75px'},
    sticky='top'
    )
    return navbar

def serveFooter():
    navbar = html.Footer([
        html.Div([
            html.P("Dział odzysku i systemów spadochronowych", className='footer-text'),
            html.P("2023", className='footer-text'),
        ], style={
                "display": "flex",
                "flex-direction": "column",
                "width": "100%",
                "height": "100%",
                "justify-content": "space-around",
                "align-items": "center"
            }
        )
    ], 
    className= 'card-footer',
    style={'height': '50px'}
    )
    return navbar

def serveInputData():
    return html.Div(
            [                
                html.H2(
                    "Podstawowe parametry symulacji",
                    style = {
                        'grid-row': '1',
                        'grid-column': '1/-1',
                    },
                    className='h2-box'
                ),
                dbc.Card([
                    dbc.CardHeader(
                        html.H3("Wyznaczenie gęstości powietrza"),
                        
                    ), 
                    dbc.CardBody([
                        html.Div(
                        [
                            "Ciśnienie odniesienia [hPa]:",
                            dcc.Input(type='number', id='input-refpressure-input', min=0, step=1, value=1013),
                            "Temperatura odniesienia [C]:",
                            dcc.Input(type='number', id='input-reftemp-input', min=0, step=.1, value=20.0),
                            "Wilgotność powietrza [%]:",
                            dcc.Input(type='number', id='input-humidity-input', min=0, step=1, max = 100, value=40),
                            "Relatywna wysokość otworzenia spadochronu [m]:",
                            dcc.Input(type='number', id='input-height-input', min=0, step=1, max=10000, value=1000),
                            "Wyznaczona gęstość powietrza [kg/m^3]:",
                            dcc.Input(type='number', id='input-airdensitycalc-input', min=0, step=1, value=0.0, disabled=True),
                        ], style={
                            "display": "grid",
                            "grid-template-columns": "1fr 75px",
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
                dbc.Card([
                    dbc.CardHeader(
                        html.H3("Parametry fizyczne"),
                    ), 
                    dbc.CardBody([
                        html.Div(
                        [
                            "Gęstość powietrza [kg/m^3]:",
                            dcc.Input(type='number', id='input-airdensity-input', min=0, step=.001, value=INPUT_PARAMETERS["AIR_DENSITY"]),
                            "Przyśpieszenie ziemskie [m/s^2]:",
                            dcc.Input(type='number', id='input-gaccel-input', min=0, step=.001, value=INPUT_PARAMETERS["G_ACCELERATION"]),
                            "Współczynnik oporu aerodynamicznego [-]:",
                            dcc.Input(type='number', id='input-dragcoeff-input', min=0, step=.001, value=INPUT_PARAMETERS["DRAG_COEFF"]),
                            "Całka oporu aerodynamicznego [-]:",
                            dcc.Input(type='number', id='input-draginteg-input', min=0, step=.001, value=INPUT_PARAMETERS["DRAG_INTEGRAL"]),
                            "Współczynnik wstrząsu przy otwarciu [-]:",
                            dcc.Input(type='number', id='input-schockfactor-input', min=0, step=.001, value=INPUT_PARAMETERS["OPENING_LOAD_SHOCK_FACTOR"]),
                            "Współczynnik redukcji siły przy otwarciu [-]:",
                            dcc.Input(type='number', id='input-forcereduction-input', min=0, step=.001, value=INPUT_PARAMETERS["OPENING_FORCE_REDUCTION_FACTOR"]),
                            "Stała napełniania czaszy [-]:",
                            dcc.Input(type='number', id='input-fillconst-input', min=0, step=.001, value=INPUT_PARAMETERS["INFLATION_CANOPY_FILL_CONST"]),
                            "Wykładnik opóźnienia [-]:",
                            dcc.Input(type='number', id='input-deccel-input', min=0, step=.001, value=INPUT_PARAMETERS["DECCELERATION_EXPONENT"]),
                        ], style={
                            "display": "grid",
                            "grid-template-columns": "1fr 75px",
                            "width": "100%",
                            "gap": "5px",
                            "text-align": "right",
                            "padding": "5px"
                        }
                        )
                    ]),
                ], style={
                    'grid-row': '2/-1',
                    'grid-column': '2',
                    'height': '100%'
                }),
                dbc.Button(
                    "Przelicz",
                    id="input-run-button",
                    style = {
                        'width': '100%',
                        'margin': '5px',
                        'background-color': BASE_COLOR,
                        'color': 'white',
                        'border-color': BASE_COLOR
                    }
                ), 
                dbc.Card([
                    dbc.CardHeader(html.H3("Opis parametrów")), 
                    dbc.CardBody([
                        html.Div(
                            id = "input-description-container",
                            style={
                                
                                "width": "100%",
                                "padding": "5px",
                                "gap": "5px"
                            }                    
                        )
                    ]),
                ], style={
                    'grid-row': '2/-1',
                    'grid-column': '3',
                    'height': '100%'
                }),
            ],
            className='input-container'
        )

def serveSim1():
    return html.Div(
            [                
                html.H2(
                    "Wymagana średnica czaszy spadochronu",
                    style = {
                        'grid-row': '1',
                        'grid-column': '1/-1',
                    },
                    className='h2-box'
                ),
                dbc.Card([
                    dbc.CardHeader(html.H3("Parametry wejściowe")), 
                    dbc.CardBody([
                        html.Div(
                        [
                            "Masa pojazdu [kg]:",
                            dcc.Input(type='number', id='simulation1-mass-input', min=0, step=.1, value=5.0),
                            "Zakres prędkości docelowej - min [m/s]:",
                            dcc.Input(type='number', id='simulation1-velocitystart-input', min=0, step=.5, value=5.0),
                            "Zakres prędkości docelowej - max [m/s]:",
                            dcc.Input(type='number', id='simulation1-velocitystop-input', min=0, step=.5, value=25.0),
                            "Oczekiwana prędkość [m/s]:",
                            dcc.Input(type='number', id='simulation1-velocity-input', min=0, step=.1, value=10.0),
                            "Wyznaczona średnica czaszy [m]:",
                            dcc.Input(type='number', id='simulation1-diameter-input', value=0.0, disabled=True),
                        ], style={
                            "display": "grid",
                            "grid-template-columns": "1fr 75px",
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
                        'background-color': BASE_COLOR,
                        'color': 'white',
                        'border-color': BASE_COLOR
                    }
                ), 
                dbc.Card([
                    dbc.CardHeader(html.H3("Wyniki")), 
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
            ],
            className='sim-container'
        )

def serveSim2():
    return html.Div(
            [                
                html.H2(
                    "Obciążenia przy otwarciu spadochronu",
                    style = {
                        'grid-row': '1',
                        'grid-column': '1/-1',
                    },
                    className='h2-box'
                ),
                dbc.Card([
                    dbc.CardHeader(
                        html.H3("Parametry wejściowe"),
                    ), 
                    dbc.CardBody([
                        html.Div(
                        [
                            "Masa pojazdu [kg]:",
                            dcc.Input(type='number', id='simulation2-mass-input', min=0, step=.1, value=5.0),
                            "Prędkość przy otwarciu [m/s]:",
                            dcc.Input(type='number', id='simulation2-velocity-input', min=0, step=.1, value=40.0),
                            "Średnica spadochronu [m]:",
                            dcc.Input(type='number', id='simulation2-diameter-input', min=0, step=.01, value=0.30),
                        ], style={
                            "display": "grid",
                            "grid-template-columns": "1fr 75px",
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
                    id="simulation2-run-button",
                    style = {
                        'width': '100%',
                        'margin': '5px',
                        'background-color': BASE_COLOR,
                        'color': 'white',
                        'border-color': BASE_COLOR
                    }
                ), 
                dbc.Card([
                    dbc.CardHeader(html.H3("Wyniki")), 
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
                    'grid-row': '2/-1',
                    'grid-column': '2',
                    'height': '100%'
                }),
            ],
            className='sim-container'
        )
