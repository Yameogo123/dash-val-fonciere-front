from dash import Dash, html, dcc, callback, Output, Input
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os
import plotly.express as px

from constantes import *
from views.tab1 import *
from views.tab2 import *
from views.tab3 import *


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets, dbc.icons.FONT_AWESOME])

app.config['suppress_callback_exceptions'] = True

app.title = "Valeur foncière"

sidebar = html.Div(
    [
        #html.Label("Valeur Foncière", className="display", style={"color": "white"}),
        html.Img(src="./assets/loc.png", style={'height':'25%','width':'80%'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink([html.I(className="bi bi-info-circle-fill me-2"), "Accueil"], href="/", active="exact"),
                dbc.NavLink("dashboard", href="/dashboard", active="exact"),
                dbc.NavLink("Prédictions", href="/prediction", active="exact"),
                #dbc.NavLink("More", href="/more", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE, 
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return Tab1
    elif pathname == "/dashboard":
        return Tab2
    elif pathname == "/prediction":
        return Tab3
    # elif pathname == "/more":
    #     return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )





if __name__ == '__main__':
    port= os.getenv("PORT") if os.getenv("PORT") is not None else 6000 
    #host="0.0.0.0"
    #app.run(debug=True, host="0.0.0.0", port= os.getenv("PORT"))
    app.run(debug= True)