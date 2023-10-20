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
import views
import constantes

from importlib import reload
reload(views)
reload(constantes)


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets])

app.config['suppress_callback_exceptions'] = True

sidebar = html.Div(
    [
        html.H4("Valeur Foncière", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Accueil", href="/", active="exact"),
                dbc.NavLink("dashboard", href="/page-1", active="exact"),
                dbc.NavLink("Prédictions", href="/page-2", active="exact"),
                dbc.NavLink("More", href="/page-3", active="exact"),
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
    elif pathname == "/page-1":
        return Tab2
    elif pathname == "/page-2":
        return Tab3
    elif pathname == "/page-3":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

#app.layout = html.Div([dcc.Location(id="url"), sidebar, content])



# app.layout = html.Div([
#     html.H1(children='Title of Dash App', style={'textAlign':'center'}),
#     dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
#     dcc.Graph(id='graph-content')
# ])



if __name__ == '__main__':
    port= os.getenv("PORT") if os.getenv("PORT") is not None else 6000 
    #host="0.0.0.0"
    app.run(debug=True, host="0.0.0.0", port= os.getenv("PORT"))
    #app.run(debug= True)