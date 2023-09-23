from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_components import themes
from dash.dependencies import Input, Output, State
import webbrowser

from structure.page import serveBody, serveNavbar
from structure.plotter import plotResults, getEmptyPlot
from Calculations.CParachute import CParachute, calculateDiameterVelocityRelationship

import numpy as np

app = Dash(__name__,
    external_stylesheets =[themes.LITERA],
    suppress_callback_exceptions=True,
    title = "PWrParaSim",
    update_title='...',
)
app._favicon = r'logo.png'

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
            serveNavbar(),
            serveBody(),
        ],
        style={
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "space-between",
            "align-items": "stretch",
            "padding": "20px 25px 20px 25px",
            "gap": "10px",
            "width": "100%"
        }
    )

app.layout = _serve_layout()

@app.callback(
    Output('simulation1-results-plot', 'figure'),
    State('simulation1-mass-input', 'value'),
    State('simulation1-velocity-input', 'value'),
    State('simulation1-velocitystart-input', 'value'),
    State('simulation1-velocitystop-input', 'value'),
    Input('simulation1-run-button', 'n_clicks')
)
def callback(fMass: float, fVelocity: float, fVelocityStart: float, fVelocityStop: float, _Button):

    try:
        aVelocity, aDiameters = calculateDiameterVelocityRelationship(
            fMass=fMass,
            tVelocityRange=(fVelocityStart, fVelocityStop),
            iSamples=100
        )

        fVelocity = aVelocity[np.argmin(np.abs(aVelocity-fVelocity))]
        fDiameter = aDiameters[np.argmin(np.abs(aVelocity-fVelocity))]

        return plotResults(aVelocity, aDiameters, sColour="black", sXlabel="Prędkość opadania [m/s]", sYLabel="Średnica czaszy spadochronu [m]", lHorizontalLines=[(fDiameter,'tomato')], lVerticalLines=[(fVelocity,'tomato')])
    except:
        return getEmptyPlot()

@app.callback(
    Output('simulation2-velocity-input', 'disabled'),
    Output('simulation2-diameter-input', 'disabled'),
    Input('simulation2-velocity-checkmark', 'value'),
    Input('simulation2-diameter-checkmark', 'value'),
)
def callback(lUseVelocity: list, lUseDiameter: list):
    return not ('use' in lUseVelocity), not ('use' in lUseDiameter)


@app.callback(
    Output('simulation2-numericdata-container', 'children'),
    State('simulation2-mass-input', 'value'),
    State('simulation2-velocity-input', 'value'),
    State('simulation2-diameter-input', 'value'),
    State('simulation2-velocity-checkmark', 'value'),
    State('simulation2-diameter-checkmark', 'value'),
    Input('simulation2-run-button', 'n_clicks')
)
def callback(fMass: float, fVelocity: float, fDiameter: float, lUseVelocity: list, lUseDiameter: list, _Button):

    try:
        cParachute = CParachute(
            fCanopyDiameter = fDiameter if 'use' in lUseDiameter else None,
            fOpenInitVelocity = fVelocity if 'use' in lUseVelocity else None,
            fMass = fMass
        )
        data = cParachute.getPeakOpeningLoad()

        sReturn = html.Pre(
f"""Masa pojazdu: {cParachute.fMass} kg.
Oczekiwana prędkość opadania: {round(cParachute.fOpenInitVelocity,3)} m.
Średnica czaszy spadochronu: {round(cParachute.fCanopyDiameter,3)} m.
Czas napełniania czaszy: {round(cParachute.fInflationTime,3)} s.
Szczytowe obciążenie przy otwarciu (parasola w rakiecie):
\t* metoda uproszczona: {round(data['simplified'],1)} N
\t* metoda Pflanz: {round(data['pflanz'],1)} N
\t* metoda OSCALC: {round(data['oscalc'],1)} N
""")
        return sReturn
    except:   
        return ""


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8080', new=2)
    app.run_server(debug=False, port=8080, host='0.0.0.0')    