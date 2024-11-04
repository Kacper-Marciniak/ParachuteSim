from dash import dcc, html
import dash_bootstrap_components as dbc
from structure.descriptions import *
from Calculations.ConstantParameters import *
from structure.ConstantParameters import *

def serveTooltip(sMessage: str, sTarget: str, sPlacement: str='top'):
    return dbc.Tooltip(
        sMessage,
        target = sTarget,
        placement = sPlacement,
        style = {
            "font-size": "16px",
        }         
    )

def serveNavbar():
    navbar = dbc.Navbar([
        html.Div([
            html.Div(
                [
                    html.A(html.Img(src=r"assets\logo_pwr.png", height="50px"), href=r'https://pwr.edu.pl/', className='logo-navbar'),
                    html.A(html.Img(src=r"assets\logo2.png", height="50px"), href=r'https://pwrinspace.pwr.edu.pl/', className='logo-navbar'),
                ], 
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "justify-content": "start",
                    "align-items": "center",
                    "gap": "5px",
                    "width": "100%"
                }
            ),
            html.Div(
                [
                    html.H1("ParaSim", style={"color": BASE_COLOR}),
                    html.Img(src=r"assets\app_shadow.png", height="50px"),
                ], 
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "justify-content": "center",
                    "align-items": "center",
                    "gap": "5px",
                    "width": "100%"
                }
            ),
            html.Div(
                [
                    html.A(html.Img(src=r"assets\logo_github.png", height="50px"), href=r'https://github.com/Kacper-Marciniak', className='logo-navbar'),
                ], 
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "justify-content": "end",
                    "align-items": "center",
                    "gap": "5px",
                    "width": "100%"
                }
            ),

        ], style={
                "display": "grid",
                "grid-template-columns": "1fr auto 1fr",
                "width": "100%",
                "height": "100%",
                "justify-content": "space-between",
                "align-items": "center",
                "padding": "0 10px 0 10px"
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
            html.P(f"ParaSim v.{APP_VERSION}", className='footer-text'),
            html.P(APP_YEAR, className='footer-text'),
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