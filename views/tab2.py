from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx, State
import dash_bootstrap_components as dbc
import sys
from views.my_map import *
sys.path.append("../")

import plotly.express as px

from constantes import *

global ann

ann= None

rep1= df[["mois", "jour", "annee", "Valeur fonciere"]].groupby(["annee", "mois", "jour"], as_index=False).agg("sum")
rep2= df.groupby('annee', as_index=False)['Valeur fonciere'].count()
rep3= df.groupby('Code type local', as_index=False)[['Valeur fonciere', 'Nombre pieces principales', 'Surface terrain']].mean()
rep4= df.groupby('Nature culture', as_index=False)[['Valeur fonciere', 'Nombre pieces principales', 'Surface terrain']].mean()
#rep3["Code type local"]= rep3["Code type local"].astype("int")

Tab2= html.Div(className='control-tab', children=[
    html.H2(className='title', children=[html.P("Exploration")]),
    html.Br(),
    dbc.Row(
        [
            dbc.Col([dcc.Slider( df['annee'].min(), df['annee'].max(),
                step=None, value=df['annee'].min(), marks={str(year): str(year) for year in df['annee'].unique()},
                id='year-slider'
            )]),
            dbc.Col([
                dbc.Button("refresh", color="danger", id="btn", n_clicks=0),
                html.Hr(),
                dbc.Toast(
                    "rafraichissement enclenché", id="positioned-toast",
                    header="Positioned toast", is_open=False,
                    dismissable=True, icon="danger",
                    duration= 2000,
                    # top: 66 positions the toast below the navbar
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                )
            ]),

        ]
    ),
    html.Div(className="head", children=[
        html.Div(className="first-row", children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div([
                            html.Div(children='Nos jeux de données'),
                            dash_table.DataTable(   
                                data=df.head(30).to_dict('records'), page_size=10, style_table={'overflowX': 'auto'}, sort_action="native",
                                sort_mode="multi"
                            )
                        ]),
                    ]
                ), style={'width': '45%', 'display': 'inline-block', 'height': '30%'}
                #className="mt-3",
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div([
                            html.Div(children='La Valeur foncière moyenne par département en France'),
                            html.Iframe(id='map', width='100%', height='370px', srcDoc=Map()._repr_html_())
                        ]),
                    ] 
                ), style={'width': '45%', 'display': 'inline-block', 'height': '30%'}
                #className="mt-3",
            ),
        
        ], style= ROW),

        html.Div(className="second-row", children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div([
                            html.Div(children='Total des valeurs foncières par période'),
                            dcc.Graph(id='graph-content', figure= px.sunburst(rep1, path=['annee', 'mois', 'jour'], values='Valeur fonciere'), responsive= True, animate= True)
                        ]),
                    ]
                ), style={'width': '45%', 'display': 'inline-block', 'height': '30%'}
                #className="mt-3",
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div([
                            html.Div(children='Evolution du nombre de vente par période'),
                            dcc.Graph(id='graph-content2', figure= px.line(rep2, x='annee', y="Valeur fonciere"), responsive= True, animate= True)
                        ]),
                    ]
                ), style={'width': '45%', 'display': 'inline-block', 'height': '30%'}
                #className="mt-3",
            )
        ], style= ROW),

        html.Br(),

        dbc.Card(
            dbc.CardBody(
                [
                    html.Div([
                        dcc.Graph(id='graph-with-slider', figure= px.bar(rep3, x="Code type local", y="Valeur fonciere", color="Code type local", title="Moyenne des valeurs foncières par type de local")),
                    ])
                ]
            )
        ),

        html.Br(),

        dbc.Card(
            dbc.CardBody(
                [
                    html.Div([
                        dcc.Graph(id='scatter-with-slider', figure=px.scatter(rep4, x="Valeur fonciere", y="Nombre pieces principales", color="Nature culture", size="Surface terrain"))
                    ])
                ]
            )
        ),
        
    ]),
    
])


@callback(
    Output("positioned-toast", "is_open"),
    Input('btn', 'n_clicks'),
    [State("positioned-toast", "is_open")])
def displayClick(_, is_open):
    if ctx.triggered_id=="btn":
        return not is_open
    return is_open 
