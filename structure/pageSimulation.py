from dash import dcc, html
import dash_bootstrap_components as dbc
from structure.plotter import getEmptyPlot
from structure.descriptions import *
from Calculations.ConstantParameters import *
from structure.baseElements import serveTooltip, BASE_COLOR

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
                    dbc.CardBody([
                        html.Div(
                            INPUT_DESCRIPTION,
                            id = "input-description-container",           
                        )
                    ], className='card-info'),
                ], style={
                    'grid-row': '2',
                    'grid-column': '1/-1',
                    'height': '100%',
                }, className='card-info'),
                dbc.Card([
                    dbc.CardHeader(
                        html.H3("Wyznaczenie gęstości powietrza"),
                    ), 
                    dbc.CardBody([
                        html.Div(
                        [
                            "Ciśnienie odniesienia [hPa]:",
                            dcc.Input(type='number', id='input-refpressure-input', min=0, step=1, value=1013),
                            serveTooltip(DESCRIPTION_AIR_DENSITY_PARAMS['refpressure'], 'input-refpressure-input'),
                            "Temperatura odniesienia [C]:",
                            dcc.Input(type='number', id='input-reftemp-input', min=0, step=.1, value=20.0),
                            serveTooltip(DESCRIPTION_AIR_DENSITY_PARAMS['reftemp'], 'input-reftemp-input'),
                            "Wilgotność powietrza [%]:",
                            dcc.Input(type='number', id='input-humidity-input', min=0, step=1, max = 100, value=40),
                            serveTooltip(DESCRIPTION_AIR_DENSITY_PARAMS['humidity'], 'input-humidity-input'),
                            "Wysokość otworzenia spadochronu [m]:",
                            dcc.Input(type='number', id='input-height-input', min=0, step=1, max=10000, value=1000),
                            serveTooltip(DESCRIPTION_AIR_DENSITY_PARAMS['height'], 'input-height-input'),
                            "Wyznaczona gęstość powietrza [kg/m^3]:",
                            dcc.Input(type='number', id='input-airdensitycalc-input', min=0, step=1, value=0.0, disabled=True),
                            serveTooltip(DESCRIPTION_AIR_DENSITY_PARAMS['airdensitycalc'], 'input-airdensitycalc-input'),
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
                    'grid-row': '3',
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
                            serveTooltip(DESCRIPTION_INPUT_PARAMS['airdensity'], 'input-airdensity-input'),
                            "Przyśpieszenie ziemskie [m/s^2]:",
                            dcc.Input(type='number', id='input-gaccel-input', min=0, step=.001, value=INPUT_PARAMETERS["G_ACCELERATION"]),
                            serveTooltip(DESCRIPTION_INPUT_PARAMS['gaccel'], 'input-gaccel-input'),
                            "Współczynnik oporu aerodynamicznego [-]:",
                            dcc.Input(type='number', id='input-dragcoeff-input', min=0, step=.001, value=INPUT_PARAMETERS["DRAG_COEFF"]),
                            serveTooltip(DESCRIPTION_INPUT_PARAMS['dragcoeff'], 'input-dragcoeff-input'),
                            "Całka oporu aerodynamicznego [-]:",
                            dcc.Input(type='number', id='input-draginteg-input', min=0, step=.001, value=INPUT_PARAMETERS["DRAG_INTEGRAL"]),
                            serveTooltip(DESCRIPTION_INPUT_PARAMS['draginteg'], 'input-draginteg-input'),
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
                        ),
                        html.Div([
                            "Kształt spadochronu:",
                            dcc.Dropdown(id='input-canopytype-dropdown', value=INPUT_PARAMETERS["CANOPY_TYPE"], options=[{'label': PARACHUTE_TYPE_LABELS[type], 'value': type} for type in AVAILABLE_CANOPY_TYPES]),
                            serveTooltip(DESCRIPTION_INPUT_PARAMS['canopytype'], 'input-canopytype-dropdown'),
                        ], style={
                            "display": "grid",
                            "grid-template-columns": "auto 1fr",
                            "width": "100%",
                            "gap": "5px",
                            "padding": "5px"
                        }
                        )
                        
                    ]),
                ], style={
                    'grid-row': '3/-1',
                    'grid-column': '2',
                    'height': '100%'
                }),
                html.Div(
                    [
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
                        dbc.Button(
                            "💾 Zapisz CSV",
                            id="input-save-button",
                            style = {
                                'width': '100%',
                                'margin': '5px',
                                'background-color': BASE_COLOR,
                                'color': 'white',
                                'border-color': BASE_COLOR
                            }
                        ),
                    ],
                    className='buttons-container'
                ),
                dbc.Card([
                    dbc.CardHeader(html.H3("Opis parametrów")), 
                    dbc.CardBody([
                        html.Pre(
                            INPUT_PARAMETERS_DESCRIPTION,
                            style={                                
                                "width": "100%",
                                "padding": "5px"
                            }                    
                        ),
                        dbc.Button(
                            "Współczynnik oporu aerodynamicznego - informacje",
                            id="input-dragcoeffinfo-button",
                            style = {
                                'width': '100%',
                                'margin': '5px',
                                'background-color': BASE_COLOR,
                                'color': 'white',
                                'border-color': BASE_COLOR
                            }
                        ),
                    ]),
                ], style={
                    'grid-row': '3/-1',
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
                    "Wymagana efektywna średnica czaszy spadochronu",
                    style = {
                        'grid-row': '1',
                        'grid-column': '1/-1',
                    },
                    className='h2-box'
                ),
                dbc.Card([
                    dbc.CardBody([
                        html.Div(
                            SIM1_DESCRIPTION,
                            id = "simulation1-description-container",                
                        )
                    ], className='card-info'),
                ], style={
                    'grid-row': '2',
                    'grid-column': '1/-1',
                    'height': '100%'
                }, className='card-info'),
                dbc.Card([
                    dbc.CardHeader(html.H3("Parametry wejściowe")), 
                    dbc.CardBody([
                        html.Div(
                        [
                            "Masa pojazdu [kg]:",
                            dcc.Input(type='number', id='simulation1-mass-input', min=0, step=.1, value=5.0),
                            serveTooltip(DESCRIPTION_SIM1_PARAMS['mass'], 'simulation1-mass-input'),
                            "Zakres prędkości docelowej - min [m/s]:",
                            dcc.Input(type='number', id='simulation1-velocitystart-input', min=0, step=.5, value=5.0),
                            serveTooltip(DESCRIPTION_SIM1_PARAMS['velocitystart'], 'simulation1-velocitystart-input'),
                            "Zakres prędkości docelowej - max [m/s]:",
                            dcc.Input(type='number', id='simulation1-velocitystop-input', min=0, step=.5, value=25.0),
                            serveTooltip(DESCRIPTION_SIM1_PARAMS['velocitystop'], 'simulation1-velocitystop-input'),
                            "Oczekiwana prędkość opadania [m/s]:",
                            dcc.Input(type='number', id='simulation1-velocity-input', min=0, step=.1, value=10.0),
                            serveTooltip(DESCRIPTION_SIM1_PARAMS['velocity'], 'simulation1-velocity-input'),
                            "Powierzchnia otworu centralnego [%]:",
                            dcc.Input(type='number', id='simulation1-holefactor-input', min=0, max=99, step=1, value=0),
                            serveTooltip(DESCRIPTION_SIM1_PARAMS['holefactor'], 'simulation1-holefactor-input'),
                            "Wyznaczona średnica czaszy [m]:",
                            dcc.Input(type='number', id='simulation1-diameter-input', value=0.0, disabled=True),
                            serveTooltip(DESCRIPTION_SIM1_PARAMS['diameter'], 'simulation1-diameter-input'),
                            "Wyznaczona średnica otworu [m]:",
                            dcc.Input(type='number', id='simulation1-holediameter-input', value=0.0, disabled=True),
                            serveTooltip(DESCRIPTION_SIM1_PARAMS['holediameter'], 'simulation1-holediameter-input'),
                            "Język etykiet na wykresie:",
                            dcc.RadioItems(['PL', 'EN'], 'EN',  id='simulation1-plotlang-radio', inline=True)
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
                    'grid-row': '3',
                    'grid-column': '1',
                    'height': '100%'
                }),
                html.Div(
                    [
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
                        dbc.Button(
                            "💾 Zapisz CSV",
                            id="simulation1-save-button",
                            style = {
                                'width': '100%',
                                'margin': '5px',
                                'background-color': BASE_COLOR,
                                'color': 'white',
                                'border-color': BASE_COLOR
                            }
                        ),
                    ],
                    className='buttons-container'
                ), 
                dbc.Card([
                    dbc.CardHeader(html.H3("Wyniki")), 
                    dbc.CardBody([
                        html.Div(
                            [
                                dcc.Graph(
                                    id = 'simulation1-results-plot',
                                    figure = getEmptyPlot(),
                                    config = {
                                        'responsive': False,
                                        'displayModeBar': True,
                                        'toImageButtonOptions': {
                                            'format': 'png',
                                            'filename': 'parasim_plot',
                                            },
                                    },
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
                    'grid-row': '3/-1',
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
                    dbc.CardBody([
                        html.Div(
                            SIM2_DESCRIPTION,
                            id = "simulation2-description-container",                  
                        )
                    ], className='card-info'),
                ], style={
                    'grid-row': '2',
                    'grid-column': '1/-1',
                    'height': '100%'
                }, className='card-info'),
                dbc.Card([
                    dbc.CardHeader(
                        html.H3("Parametry wejściowe"),
                    ), 
                    dbc.CardBody([
                        html.Div(
                        [
                            "Masa pojazdu [kg]:",
                            dcc.Input(type='number', id='simulation2-mass-input', min=0, step=.1, value=5.0),
                            serveTooltip(DESCRIPTION_SIM2_PARAMS['mass'], 'simulation2-mass-input'),
                            "Prędkość przy otwarciu [m/s]:",
                            dcc.Input(type='number', id='simulation2-velocity-input', min=0, step=.1, value=40.0),
                            serveTooltip(DESCRIPTION_SIM2_PARAMS['velocity'], 'simulation2-velocity-input'),
                            "Średnica spadochronu [m]:",
                            dcc.Input(type='number', id='simulation2-diameter-input', min=0, step=.01, value=0.30),
                            serveTooltip(DESCRIPTION_SIM2_PARAMS['diameter'], 'simulation2-diameter-input'),
                            "Średnica otworu centralnego [m]:",
                            dcc.Input(type='number', id='simulation2-holediameter-input', min=0, step=.01, value=0.0),
                            serveTooltip(DESCRIPTION_SIM2_PARAMS['holediameter'], 'simulation2-holediameter-input'),
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
                    'grid-row': '3',
                    'grid-column': '1',
                    'height': '100%'
                }),
                html.Div(
                    [
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
                        dbc.Button(
                            "💾 Zapisz CSV",
                            id="simulation2-save-button",
                            style = {
                                'width': '100%',
                                'margin': '5px',
                                'background-color': BASE_COLOR,
                                'color': 'white',
                                'border-color': BASE_COLOR
                            }
                        ),
                    ],
                    className='buttons-container'
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
                    'grid-row': '3/-1',
                    'grid-column': '2',
                    'height': '100%'
                }),
            ],
            className='sim-container'
        )

def serveShapeGenerator():
    return html.Div(
            [                
                html.H2(
                    "Generator kształtu czaszy spadochronu",
                    style = {
                        'grid-row': '1',
                        'grid-column': '1/-1',
                    },
                    className='h2-box'
                ),
                dbc.Card([
                    dbc.CardBody([
                        html.Div(
                            GENERATOR_DESCRIPTION,
                            id = "shapegenerator-description-container",                    
                        )
                    ], className='card-info'),
                ], style={
                    'grid-row': '2',
                    'grid-column': '1/-1',
                    'height': '100%'
                }, className='card-info'),
                dbc.Card([
                    dbc.CardHeader(
                        html.H3("Parametry wejściowe"),
                    ), 
                    dbc.CardBody([
                        html.Div(
                        [
                            "Efektywna średnica spadochronu [m]:",
                            dcc.Input(type='number', id='shapegenerator-diameter-input', min=0, step=.01, value=0.30),
                            serveTooltip(DESCRIPTION_GENERATOR_PARAMS['diameter'], 'shapegenerator-diameter-input'),
                            "Liczba segmentów [-]:",
                            dcc.Input(type='number', id='shapegenerator-segments-input', min=5, step=1, value=8),
                            serveTooltip(DESCRIPTION_GENERATOR_PARAMS['segments'], 'shapegenerator-segments-input'),
                            "Współczynnik sferyczności [%]:",
                            dcc.Input(type='number', id='shapegenerator-spherepercent-input', min=5, max=95, step=1, value=50),
                            serveTooltip(DESCRIPTION_GENERATOR_PARAMS['spherepercent'], 'shapegenerator-spherepercent-input'),
                            "Kąt rozwarcia stożka [deg]:",
                            dcc.Input(type='number', id='shapegenerator-coneangle-input', min=1, max=179, step=1, value=135),
                            serveTooltip(DESCRIPTION_GENERATOR_PARAMS['coneangle'], 'shapegenerator-coneangle-input'),
                            "Średnica centralnego otworu [m]:",
                            dcc.Input(type='number', id='shapegenerator-holediameter-input', min=0, step=.01, value=0),
                            serveTooltip(DESCRIPTION_GENERATOR_PARAMS['holediameter'], 'shapegenerator-holediameter-input'),
                            "Liczba punktów [-]:",
                            dcc.Input(type='number', id='shapegenerator-points-input', min=2, max=250, step=1, value=15),
                            serveTooltip(DESCRIPTION_GENERATOR_PARAMS['points'], 'shapegenerator-points-input'),
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
                    'grid-row': '3',
                    'grid-column': '1',
                    'height': '100%'
                }),
                html.Div(
                    [
                        dbc.Button(
                            "Przelicz",
                            id="shapegenerator-run-button",
                            style = {
                                'width': '100%',
                                'margin': '5px',
                                'background-color': BASE_COLOR,
                                'color': 'white',
                                'border-color': BASE_COLOR
                            }
                        ),
                        dbc.Button(
                            "💾 Zapisz DXF",
                            id="shapegenerator-save-button",
                            style = {
                                'width': '100%',
                                'margin': '5px',
                                'background-color': BASE_COLOR,
                                'color': 'white',
                                'border-color': BASE_COLOR
                            }
                        ),
                    ],
                    className='buttons-container'
                ),
                dbc.Card([
                    dbc.CardHeader(html.H3("Wyniki - 2D")), 
                    dbc.CardBody([
                        html.Div(
                            [
                                dcc.Graph(
                                    id = 'shapegenerator-results-plot',
                                    figure = getEmptyPlot(),
                                    config = {
                                        'responsive': False,
                                        'displayModeBar': True,
                                        'toImageButtonOptions': {
                                            'format': 'png',
                                            'filename': 'parasim_plot',
                                            },
                                    },
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
                    'grid-row': '3/5',
                    'grid-column': '2',
                    'height': '100%'
                }),
                dbc.Card([
                    dbc.CardHeader(html.H3("Wyniki - 3D")), 
                    dbc.CardBody([
                        html.Div(
                            [
                                dcc.Graph(
                                    id = 'shapegenerator-results2-plot',
                                    figure = getEmptyPlot(),
                                    config = {
                                        'responsive': False,
                                        'displayModeBar': True,
                                        'toImageButtonOptions': {
                                            'format': 'png',
                                            'filename': 'parasim_plot',
                                            },
                                    },
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
                    'grid-row': '3/5',
                    'grid-column': '3',
                    'height': '100%'
                }),
                dbc.Card([
                    dbc.CardBody(
                    [],
                    className='card-info',
                    id = "shapegenerator-alert-container",
                    ),
                ], style={
                    'grid-row': '5',
                    'grid-column': '1/-1',
                    'height': '100%'
                }, className='card-alert'),
            ],
            className='shape-container'
        )

def serveModalDragCoeffInfo():
    modal = dbc.Modal([
        dbc.ModalHeader(html.H2("Współczynnik oporu aerodynamicznego")),
        dbc.ModalBody([
            html.Div(
                [
                    html.H3("Kształt spadochronu"),
                    html.H3("Współczynnik"),
                ] + [val for row in [(html.B(PARACHUTE_TYPE_LABELS[key]), val) for key,val in COEFF_INFO.items()] for val in row],
                style={
                    "display": "grid",
                    "grid-template-columns": "1fr auto",
                    "width": "100%",
                    "gap": "10px",
                    "text-align": "right",
                    "padding": "5px"
                }
            )
        ]),
    ], id='modal-dragcoeffinfo', is_open=False)
    return modal