import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sub
import plotly.express as px

from dash import html

def getEmptyPlot():
    return {
        "layout": {
            "xaxis": {
                "visible": False
            },
            "yaxis": {
                "visible": False
            },
            "annotations": [
                {
                    "text": "Brak danych",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        }
    }

def plotResults(aXArray: np.ndarray, aYArray: np.ndarray, sXlabel: str = "", sYLabel: str = "", sColour: str = "black", lHorizontalLines: list[tuple] = [], lVerticalLines: list[tuple] = []):

    dcFigure = go.Figure()

    dcFigure.add_trace(
        go.Scatter(
            x = aXArray, 
            y = aYArray,
            line_color=sColour,
            mode='lines',
            showlegend=False,
            hoverinfo='text',
            hovertemplate="Średnica: %{y:.3f}<extra></extra>",
            opacity=0.75,
        )
    )

    for fY,sColor in lHorizontalLines:
        dcFigure.add_hline(
            fY,
            line_color = sColor, 
            opacity = .75, 
            line_width = 2, 
            layer = 'below'
        )

    for fX,sColor in lVerticalLines:
        dcFigure.add_vline(
            fX,
            line_color = sColor, 
            opacity = .75, 
            line_width = 2, 
            layer = 'below'
        )

    dcYaxis = dict(title_text = sYLabel, showticklabels=True, tickfont=dict(size=12))
    dcXaxis = dict(title_text = sXlabel, showticklabels=True, tickfont=dict(size=12))
    dcMargin = dict(l = 15, r = 5, t = 0, b = 0)

    dcFigure.update_layout(
        transition_duration = 200, 
        autosize = True,
        template = "seaborn",
        xaxis = dcXaxis,
        yaxis = dcYaxis,
        margin = dcMargin,
        showlegend = False,
        hovermode = "x unified",
    )

    return {'data': dcFigure['data'],'layout': dcFigure['layout']}