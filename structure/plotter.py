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

def plotResults(aXArray: np.ndarray, aYArray: np.ndarray, sXlabel: str = "", sYLabel: str = "", sColour: str = "black", lHorizontalLines: list[tuple] = [], lVerticalLines: list[tuple] = [], bEqualAxis: bool = False):

    dcFigure = go.Figure()

    dcFigure.add_trace(
        go.Scatter(
            x = aXArray, 
            y = aYArray,
            line_color=sColour,
            mode='lines',
            showlegend=False,
            hoverinfo='text',
            hovertemplate="Średnica: %{y:.3f} m<extra></extra>",
            opacity=0.90,
        )
    )

    for fY,sColor in lHorizontalLines:
        dcFigure.add_hline(
            fY,
            line_color = sColor,
            line_dash = "dash",
            opacity = 0.90, 
            line_width = 2, 
            layer = 'below',
        )

    for fX,sColor in lVerticalLines:
        dcFigure.add_vline(
            fX,
            line_color = sColor, 
            line_dash = "dash",
            opacity = 0.90, 
            line_width = 2, 
            layer = 'below'
        )

    dcYaxis = dict(
        title_text = sYLabel,
        showticklabels=True,
        tickfont=dict(size=12),
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        scaleanchor="x" if bEqualAxis else "y",
    )
    dcXaxis = dict(
        title_text = sXlabel,
        showticklabels=True,
        tickfont=dict(size=12),
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
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
        plot_bgcolor='white',
    )

    return {'data': dcFigure['data'],'layout': dcFigure['layout']}

def plotShape(aXArray: np.ndarray, aYArray: np.ndarray, sColour: str = "black"):

    dcFigure = go.Figure()

    dcFigure.add_trace(
        go.Scatter(
            x = aXArray, 
            y = aYArray,
            line_color=sColour,
            mode='lines',
            showlegend=False,
            hoverinfo='text',
            hovertemplate="X:%{x:.3f} Y:%{y:.3f} m<extra></extra>",
            opacity=0.90,
        )
    )

    # Add text
    dcFigure.add_trace(
        go.Scatter(
            x = [np.min(aXArray)], 
            y = [np.max(aYArray)],
            text = f"SX={np.max(aXArray)-np.min(aXArray):.3f}m; SY={np.max(aYArray)-np.min(aYArray):.3f}m",
            mode = "text",
            textfont=dict(size=16),
            showlegend=False,
            hoverinfo='none',
            opacity=0.90,
        )
    )

    # Add axis
    dcFigure.add_hline(
        0,
        line_color = "red",
        opacity = 1, 
        line_width = 1,
    )    
    dcFigure.add_vline(
        0,
        line_color = "red", 
        opacity = 1, 
        line_width = 1,
    )

    dcYaxis = dict(
        showticklabels=True,
        tickfont=dict(size=12),
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        scaleanchor="x",
    )
    dcXaxis = dict(
        showticklabels=True,
        tickfont=dict(size=12),
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    dcMargin = dict(l = 15, r = 5, t = 0, b = 0)

    dcFigure.update_layout(
        transition_duration = 200, 
        autosize = True,
        template = "seaborn",
        xaxis = dcXaxis,
        yaxis = dcYaxis,
        margin = dcMargin,
        showlegend = False,
        plot_bgcolor='white',
    )

    return {'data': dcFigure['data'],'layout': dcFigure['layout']}


def plotShape3D(fSphereRadius: float, fSpherePercent: float, fHolePercent: float, iNumberOfSegments: int):

    dcFigure = go.Figure()

    STEPS_U_SEGMENT = round((1.0/iNumberOfSegments)*360)
    STEPS_U_REST = 360-STEPS_U_SEGMENT
    STEPS_O = 180

    # ADD SINGLE SEGMENT

    u, v = np.meshgrid(np.linspace(0,2*np.pi/iNumberOfSegments,STEPS_U_SEGMENT), np.linspace(0,np.pi,STEPS_O))

    x = fSphereRadius * np.cos(u)*np.sin(v)
    y = fSphereRadius * np.sin(u)*np.sin(v)
    z = fSphereRadius * np.cos(v)

    indices = np.logical_and(z <= (1-fHolePercent)*2*fSphereRadius-fSphereRadius, z >= (1-fSpherePercent)*2*fSphereRadius-fSphereRadius)

    x[~indices] = np.nan
    y[~indices] = np.nan
    z[~indices] = np.nan

    # Add surface trace
    dcFigure.add_trace(
        go.Surface(
            x=x,
            y=y,
            z=z,
            showlegend=False,
            hoverinfo='none',
            opacity=1.0,
            colorscale = [[0, 'crimson'], [1, 'crimson']],
            showscale = False,
        )
    )

    # ADD THE REST

    u, v = np.meshgrid(np.linspace(2*np.pi/iNumberOfSegments,2*np.pi,STEPS_U_REST), np.linspace(0,np.pi,STEPS_O))

    x = fSphereRadius * np.cos(u)*np.sin(v)
    y = fSphereRadius * np.sin(u)*np.sin(v)
    z = fSphereRadius * np.cos(v)

    indices = np.logical_and(z <= (1-fHolePercent)*2*fSphereRadius-fSphereRadius, z >= (1-fSpherePercent)*2*fSphereRadius-fSphereRadius)

    x[~indices] = np.nan
    y[~indices] = np.nan
    z[~indices] = np.nan

    # Add surface trace
    dcFigure.add_trace(
        go.Surface(
            x=x,
            y=y,
            z=z,
            showlegend=False,
            hoverinfo='none',
            opacity=0.50,
            colorscale = [[0, 'royalblue'], [1, 'royalblue']],
            showscale = False,
        )
    )


    # Add axis
    dcFigure.add_trace(
        go.Scatter3d(
            x=[0,0],
            y=[0,0],
            z=[np.nanmin(z),fSphereRadius],
            mode='lines',
            line=dict(color='black', width=1),
            showlegend=False,
            hoverinfo='none',
            opacity=1,
        )
    )
    dcMargin = dict(l = 15, r = 5, t = 0, b = 0)

    dcFigure.update_layout(
        transition_duration = 200, 
        autosize = True,
        template = "seaborn",
        margin = dcMargin,
        showlegend = False,
        plot_bgcolor='white',
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        )
    )

    return {'data': dcFigure['data'],'layout': dcFigure['layout']}