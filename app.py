from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash_bootstrap_components import themes
from dash.dependencies import Input, Output, State
import webbrowser
import pandas as pd
import datetime
import ezdxf
from ezdxf import units
import os

from structure.pageSimulation import serveSim1, serveSim2, serveInputData, serveShapeGenerator, serveModalDragCoeffInfo
from structure.baseElements import serveNavbar, serveFooter
from structure.plotter import plotResults, plotShape, plotShape3D, getEmptyPlot
from Calculations.CParachute import CParachute, calculateDiameterVelocityRelationship
from Calculations.CShapeGenerator import CShapeGenerator
from Calculations.Air import getAirDensity
from Calculations.ConstantParameters import INPUT_PARAMETERS, KELVIN_OFFSET

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
        dcc.Store('airdensity-results-store', storage_type='session', data={}),
        dcc.Store('input-parameters-store', storage_type='session', data=INPUT_PARAMETERS),
        dcc.Store('simulation1-results-store', storage_type='session', data={}),
        dcc.Store('simulation2-results-store', storage_type='session', data={}),
        dcc.Store('shapegenerator-results-store', storage_type='session', data=[]),
        dcc.Download('airdensity-results-download'),
        dcc.Download('simulation1-results-download'),
        dcc.Download('simulation2-results-download'),
        dcc.Download('shapegenerator-results-download')
    ])

# Update displayed page
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(sUrl: str | None):
    return html.Div(
        [
            serveNavbar(),
            html.Div([
                serveInputData(),
                serveSim1(),
                serveSim2(),
                serveShapeGenerator(),
                ],
                className='page-content-body'
            ),
            serveFooter(),
            serveModalDragCoeffInfo()
        ],
        className='page-content'
    )

app.layout = _serve_layout()

@app.callback(
    Output('input-airdensity-input', 'value'),
    Output('input-airdensitycalc-input', 'value'),
    Output('input-airdensity-input', 'style'),
    Output('input-airdensitycalc-input', 'style'),
    Output('airdensity-results-store', 'data'),
    State('input-refpressure-input', 'value'),
    State('input-reftemp-input', 'value'),
    State('input-height-input', 'value'),
    State('input-humidity-input', 'value'),    
    State('input-parameters-store', 'data'),
    Input('input-run-button', 'n_clicks'),
    Input('input-airdensity-input', 'value')
)
def callback(fRefPressure: float, fRefTemp: float, fHeight: float, fHumidity: float, dcStore: dict, _Button, _ValAirInput): 
    sTrigger = callback_context.triggered_id
    if sTrigger == 'input-airdensity-input':
        dcStyle = {"background-color": "white"}
        return no_update, None, dcStyle, dcStyle, {}
    if _Button: 
        try:    
            fRefPressure *= 100
            fRefTemp += KELVIN_OFFSET # Celcius degrees to Kelvins
            fHeight *= -1.0
            fHumidity /= 100.0
            fDensity = round(getAirDensity(fRefPressure, fRefTemp, fHeight, fHumidity, dcParameters = dcStore),3)
            dcStyle = {"background-color": "rgba(75,75,225, 0.5)"}
            dcData = {
                "Referencyjne ciśnienie atmosferyczne [hPa]": round(fRefPressure,1),
                "Referencyjna temperatura powietrza [C]": round(fRefTemp,1),
                "Względna wysokość otwarcia spadochronu [m]": fHeight,
                "Referencyjna wilgotność powietrza [%]": round(fHumidity*100.0),
                "Gęstość powietrza [kg/m3]]": round(fDensity,3),
            }
            return fDensity, fDensity, dcStyle, dcStyle, dcData
        except Exception as E:
            print(E)
    return no_update, no_update, no_update, no_update, {}

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
    Output('simulation1-results-store', 'data'),
    State('simulation1-mass-input', 'value'),
    State('simulation1-velocity-input', 'value'),
    State('simulation1-velocitystart-input', 'value'),
    State('simulation1-velocitystop-input', 'value'),
    State('input-parameters-store', 'data'),
    State('simulation1-plotlang-radio', 'value'),
    Input('simulation1-run-button', 'n_clicks')
)
def callback(fMass: float, fVelocity: float, fVelocityStart: float, fVelocityStop: float, dcParameters: dict, sLanguage: str, _Button):
    if _Button:
        try:
            bIsPL = sLanguage=="PL"
            aVelocity, aDiameters = calculateDiameterVelocityRelationship(
                fMass=fMass,
                tTargetVelocityRange=(fVelocityStart, fVelocityStop),
                iSamples=100,
                dcParameters=dcParameters
            )

            fVelocity = aVelocity[np.argmin(np.abs(aVelocity-fVelocity))]
            fDiameter = aDiameters[np.argmin(np.abs(aVelocity-fVelocity))]
            
            dcData = {
                "Masa pojazdu [kg]": fMass,
                "Docelowa prędkość opadania [m/s]": round(fVelocity,3),
                "Średnica czaszy spadochronu [m]": round(fDiameter,3),
            }

            return plotResults(
                aVelocity, aDiameters, 
                sColour="black", 
                sXlabel="Docelowa prędkość opadania [m/s]" if bIsPL else "Target descent velocity [m/s]", 
                sYLabel="Średnica czaszy [m]" if bIsPL else "Canopy diameter [m]", 
                lHorizontalLines=[(fDiameter,'crimson')], lVerticalLines=[(fVelocity,'crimson')]
            ), np.round(fDiameter,2), dcData
        except Exception as E:
            print(E)
    return getEmptyPlot(), 0.0, {}


@app.callback(
    Output('simulation2-numericdata-container', 'children'),
    Output('simulation2-results-store', 'data'),
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
            dcData = {
                "Masa pojazdu [kg]": cParachute.fMass,
                "Prędkość przy otwarciu [m/s]": round(cParachute.fOpenInitVelocity,3),
                "Średnica czaszy spadochronu [m]": round(cParachute.fCanopyDiameter,3),
                "Czas napełniania czaszy [s]": round(cParachute.fInflationTime,3),
                "Parametr balistyczny [-]": round(fBallisticParam,3),
                "Szczytowe obciążenie (Pflanz) [N]": round(dcDataLoad['pflanz'],1),
                "Szczytowe obciążenie (OSCALC) [N]": round(dcDataLoad['oscalc'],1),
            }
            return sReturn, dcData
        except Exception as E: 
            print(E)  
    
    return "Brak danych", {}
    
@app.callback(
    Output('shapegenerator-results-plot', 'figure'),    
    Output('shapegenerator-results2-plot', 'figure'),    
    Output('shapegenerator-results-store', 'data'),
    State('shapegenerator-diameter-input', 'value'),
    State('shapegenerator-segments-input', 'value'),
    State('shapegenerator-spherepercent-input', 'value'),
    State('shapegenerator-points-input', 'value'),
    State('shapegenerator-holediameter-input', 'value'),
    Input('shapegenerator-run-button', 'n_clicks')
)
def callback(fDiameter: float, iSegments: int, fSpherePercent: float, iNPoints: int, fHoleDiameter: float, _Button):
    if _Button:
        try:
            cGenerator = CShapeGenerator(fSpherePercent, fDiameter, iSegments, fHoleDiameter)
            aContour = cGenerator.getSegmentShape(iNPoints)

            return plotShape(
                aContour[:,1], aContour[:,0], 
                sColour="black"
            ), plotShape3D(
                cGenerator.fSphereRadius,
                cGenerator.fSpherePercent,
                cGenerator.fHolePercent,
                cGenerator.iNumberOfSegments
            ), aContour.tolist()
        except Exception as E:
            print(E)
    return getEmptyPlot(), getEmptyPlot(), []

@app.callback(
    Output('simulation1-mass-input', 'value'),
    Output('simulation2-mass-input', 'value'),
    Output('simulation1-mass-input', 'style'),
    Output('simulation2-mass-input', 'style'),
    Input('simulation1-mass-input', 'value'),
    Input('simulation2-mass-input', 'value'),
)
def callback(fMass1: float, fMass2: float):
    sTrigger = callback_context.triggered_id
    if sTrigger == 'simulation1-mass-input':
        dcStyle2 = {"background-color": "rgba(75,225,25, 0.5)"}
        dcStyle1 = {"background-color": "white"}
        return fMass1, fMass1, dcStyle1, dcStyle2
    elif sTrigger == 'simulation2-mass-input':
        dcStyle1 = {"background-color": "rgba(75,225,25, 0.5)"}
        dcStyle2 = {"background-color": "white"}
        return fMass2, fMass2, dcStyle1, dcStyle2
    else:
        return no_update, no_update, no_update, no_update

@app.callback(
    Output('simulation2-diameter-input', 'value'),
    Output('shapegenerator-diameter-input', 'value'),
    Output('simulation1-diameter-input', 'style'),
    Output('simulation2-diameter-input', 'style'),
    Output('shapegenerator-diameter-input', 'style'),
    Input('simulation1-diameter-input', 'value'),
    Input('simulation2-diameter-input', 'value'),
    Input('shapegenerator-diameter-input', 'value')
)
def callback(fDiameter: float, _Sim2Val, _GenVal):
    sTrigger = callback_context.triggered_id
    if sTrigger == 'simulation1-diameter-input':
        dcStyle = {"background-color": "rgba(75,225,25, 0.5)"} if fDiameter>0.0 else {"background-color": "white"}
        return fDiameter, fDiameter, dcStyle, dcStyle, dcStyle
    elif sTrigger == 'simulation2-diameter-input' or sTrigger == 'shapegenerator-diameter-input':
        dcStyle = {"background-color": "white"}
        return no_update, no_update, dcStyle, dcStyle, dcStyle
    else:
        return no_update, no_update, no_update, no_update, no_update


@app.callback(
    Output('airdensity-results-download', 'data'),
    State('airdensity-results-store', 'data'),
    Input('input-save-button', 'n_clicks')
)
def callback(dcData: dict, _Button):

    if _Button:
        try:
            sName = 'wyniki_gestosc_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
            pdData = pd.DataFrame().from_dict({key: [dcData[key]] for key in dcData})
            return dcc.send_data_frame(pdData.to_csv, sName, sep = ';', index = False, header=True, encoding='utf-8')
        except Exception as E: 
            print(E)  
    return no_update

@app.callback(
    Output('simulation1-results-download', 'data'),
    State('simulation1-results-store', 'data'),
    Input('simulation1-save-button', 'n_clicks')
)
def callback(dcData: dict, _Button):

    if _Button:
        try:
            sName = 'wyniki_srednica_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
            pdData = pd.DataFrame().from_dict({key: [dcData[key]] for key in dcData})
            return dcc.send_data_frame(pdData.to_csv, sName, sep = ';', index = False, header=True, encoding='utf-8')
        except Exception as E: 
            print(E)  
    return no_update

@app.callback(
    Output('simulation2-results-download', 'data'),
    State('simulation2-results-store', 'data'),
    Input('simulation2-save-button', 'n_clicks')
)
def callback(dcData: dict, _Button):

    if _Button:
        try:
            sName = 'wyniki_obciazenia_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
            pdData = pd.DataFrame().from_dict({key: [dcData[key]] for key in dcData})
            return dcc.send_data_frame(pdData.to_csv, sName, sep = ';', index = False, header=True, encoding='utf-8')
        except Exception as E: 
            print(E)  
    return no_update

@app.callback(
    Output('shapegenerator-results-download', 'data'),
    State('shapegenerator-results-store', 'data'),
    Input('shapegenerator-save-button', 'n_clicks')
)
def callback(lData: list, _Button):

    if _Button:
        try:
            sName = 'parachute_{}.dxf'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
            _Dxf = ezdxf.new('R2000')
            _Dxf.header['$MEASUREMENT'] = 1
            _Dxf.units = units.M
            _Dxf.layers.new(name="parachute", dxfattribs={"color": 0})
            msp = _Dxf.modelspace()
            msp.add_polyline2d(lData, dxfattribs={"layer": "parachute", "lineweight": 20})

            _Dxf.saveas(sName)
            with open(sName, 'r') as f:
                content = f.read()

            os.remove(sName)

            return dict(content=content, filename=sName)
        except Exception as E: 
            print(E)  
    return no_update

@app.callback(
    Output('modal-dragcoeffinfo', 'is_open'),
    Input('input-dragcoeffinfo-button', 'n_clicks')
)
def callback(_Button):
    if _Button:
        return True
    else:    
        return no_update

if __name__ == '__main__':
    webbrowser.open(r'http://127.0.0.1:8080', new=2)
    app.run_server(debug=False, port=8080, host='0.0.0.0')