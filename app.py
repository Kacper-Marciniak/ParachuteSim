from dash import Dash, dcc, html, dash_table, callback_context, no_update
import dash_bootstrap_components as dbc
from dash_bootstrap_components import themes
from dash.dependencies import Input, Output, State
import webbrowser

from structure.page import serveSim1, serveSim2, serveNavbar, serveFooter, serveInputData
from structure.plotter import plotResults, getEmptyPlot
from calculations.CParachute import CParachute, calculateDiameterVelocityRelationship
from calculations.Air import getAirDensity
from calculations.ConstantParameters import INPUT_PARAMETERS, KELVIN_OFFSET

import numpy as np

app = Dash(__name__,
    external_stylesheets =[themes.LITERA],
    suppress_callback_exceptions=True,
    title = "ParaSim",
    update_title='...',
)
app._favicon = r'app.png'

def _serve_layout():
    return html.Div([
        html.Meta(charSet="utf-8"),
        dcc.Location(id='url', refresh=True),
        html.Div(id='page-content'),
        html.Div(id='hidden-container', style={'display':'none'}),
    ])

# Update displayed page
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(sUrl: str | None):
    return html.Div(
        [
            dcc.Store(id='input-parameters-store', storage_type='session', data=INPUT_PARAMETERS),
            serveNavbar(),
            serveInputData(),
            serveSim1(),
            serveSim2(),
            serveFooter(),            
        ],
        style={
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "space-between",
            "align-items": "stretch",
            "padding": "20px 25px 20px 25px",
            "gap": "10px",
            "width": "100%",
            "min-height": "100vh",
            "min-width": "1280px"
        }
    )

app.layout = _serve_layout()

@app.callback(
    Output('input-airdensity-input', 'value'),
    Output('input-airdensitycalc-input', 'value'),
    State('input-refpressure-input', 'value'),
    State('input-reftemp-input', 'value'),
    State('input-height-input', 'value'),
    State('input-humidity-input', 'value'),    
    State('input-parameters-store', 'data'),
    Input('input-run-button', 'n_clicks')
)
def callback(fRefPressure: float, fRefTemp: float, fHeight: float, fHumidity: float, dcStore: dict, _Button): 
    if _Button: 
        try:    
            fRefPressure *= 100
            fRefTemp += KELVIN_OFFSET # Celcius degrees to Kelvins
            fHeight *= -1.0
            fHumidity /= 100.0
            fDensity = round(getAirDensity(fRefPressure, fRefTemp, fHeight, fHumidity, dcParameters = dcStore),3)
            return fDensity, fDensity
        except Exception as E:
            print(E)
    return no_update, no_update

@app.callback(
    Output('input-parameters-store', 'data'),
    Input('input-airdensity-input', 'value'),
    Input('input-gaccel-input', 'value'),
    Input('input-dragcoeff-input', 'value'),
    Input('input-schockfactor-input', 'value'),
    Input('input-forcereduction-input', 'value'),
    Input('input-fillconst-input', 'value'),
    Input('input-deccel-input', 'value'),
    Input('input-draginteg-input', 'value'),
    State('input-parameters-store', 'data')
)
def callback(fAirDensity: float, fGAccel: float, fDragCoeff: float, fSchockFactor: float, fForceReduction: float, fFillConst: float, fDeccelExp: float, fDragInteg: float, dcStore: dict):
    dcStore["AIR_DENSITY"] = fAirDensity
    dcStore["DRAG_COEFF"] = fDragCoeff
    dcStore["G_ACCELERATION"] = fGAccel
    dcStore["OPENING_LOAD_SHOCK_FACTOR"] = fSchockFactor
    dcStore["OPENING_FORCE_REDUCTION_FACTOR"] = fForceReduction
    dcStore["INFLATION_CANOPY_FILL_CONST"] = fFillConst
    dcStore["DECCELERATION_EXPONENT"] = fDeccelExp
    dcStore["DRAG_INTEGRAL"] = fDragInteg
    return dcStore

@app.callback(
    Output('simulation1-results-plot', 'figure'),
    Output('simulation1-diameter-input', 'value'),
    State('simulation1-mass-input', 'value'),
    State('simulation1-velocity-input', 'value'),
    State('simulation1-velocitystart-input', 'value'),
    State('simulation1-velocitystop-input', 'value'),
    State('input-parameters-store', 'data'),
    Input('simulation1-run-button', 'n_clicks')
)
def callback(fMass: float, fVelocity: float, fVelocityStart: float, fVelocityStop: float, dcParameters: dict, _Button):

    if _Button:
        try:
            aVelocity, aDiameters = calculateDiameterVelocityRelationship(
                fMass=fMass,
                tTargetVelocityRange=(fVelocityStart, fVelocityStop),
                iSamples=100,
                dcParameters=dcParameters
            )

            fVelocity = aVelocity[np.argmin(np.abs(aVelocity-fVelocity))]
            fDiameter = aDiameters[np.argmin(np.abs(aVelocity-fVelocity))]

            return plotResults(
                aVelocity, aDiameters, 
                sColour="black", 
                sXlabel="Prędkość docelowa [m/s]", sYLabel="Średnica czaszy [m]", 
                lHorizontalLines=[(fDiameter,'tomato')], lVerticalLines=[(fVelocity,'tomato')]
            ), np.round(fDiameter,2)
        except Exception as E:
            print(E)
    return getEmptyPlot(), 0.0


@app.callback(
    Output('simulation2-numericdata-container', 'children'),
    State('simulation2-mass-input', 'value'),
    State('simulation2-velocity-input', 'value'),
    State('simulation2-diameter-input', 'value'),
    State('input-parameters-store', 'data'),
    Input('simulation2-run-button', 'n_clicks')
)
def callback(fMass: float, fVelocity: float, fDiameter: float, dcParameters: dict, _Button):

    if _Button:
        try:
            cParachute = CParachute(
                fCanopyDiameter = fDiameter,
                fOpenInitVelocity = fVelocity,
                fMass = fMass,
                dcParameters = dcParameters,
            )
            dcDataLoad = cParachute.getPeakOpeningLoad()
            fBallisticParam = cParachute.getBallisticParameter()

            sReturn = html.Pre(
    f"""Masa pojazdu: {cParachute.fMass} kg.
Prędkość przy otwarciu: {round(cParachute.fOpenInitVelocity,3)} m/s.
Średnica czaszy spadochronu: {round(cParachute.fCanopyDiameter,3)} m.
Czas napełniania czaszy: {round(cParachute.fInflationTime,3)} s.
Parametr balistyczny: {round(fBallisticParam,3)}.
Szczytowe obciążenie przy otwarciu:
\t* metoda Pflanz: {round(dcDataLoad['pflanz'],1)} N
\t* metoda OSCALC: {round(dcDataLoad['oscalc'],1)} N"""
                )
            return sReturn
        except Exception as E: 
            print(E)  
    
    return "Brak danych"
    

@app.callback(
    Output('simulation1-mass-input', 'value'),
    Output('simulation2-mass-input', 'value'),
    Input('simulation1-mass-input', 'value'),
    Input('simulation2-mass-input', 'value'),
)
def callback(fMass1: float, fMass2: float):
    sTrigger = callback_context.triggered_id
    if sTrigger == 'simulation1-mass-input':
        return fMass1, fMass1
    elif sTrigger == 'simulation2-mass-input':
        return fMass2, fMass2
    else:
        return no_update, no_update

@app.callback(
    Output('simulation2-diameter-input', 'value'),
    Input('simulation1-diameter-input', 'value'),
)
def callback(fDiameter: float):
    sTrigger = callback_context.triggered_id
    if sTrigger == 'simulation1-diameter-input':
        return fDiameter
    else:
        return no_update


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8080', new=2)
    app.run_server(debug=False, port=8080, host='0.0.0.0')    