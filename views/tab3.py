from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc
import sys
sys.path.append("../")
from constantes import *
import datetime

import requests
import base64
import io


form = dbc.Col(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Choix de la commune", html_for="commune"),
                        dcc.Dropdown(
                            id="commune",
                            options=list(df["Commune"].unique()),
                            searchable= True, placeholder="Faites un choix * "
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Label("Choix du département", html_for="departement"),
                        dcc.Dropdown(
                            id="departement",
                            options=list(df["Departement"].unique()),
                            searchable= True, placeholder="Faites un choix * "
                        ),
                    ],
                    width=6,
                ),
            ],
            className="g-3",
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Surface terrain", html_for="surface"),
                        dbc.Input(
                            type="number", id="surface",
                            placeholder="Veuillez saisir la surface"
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Label("Nombre pieces principales", html_for="piece"),
                        dbc.Input(
                            type="number", id="piece",
                            placeholder="Veuillez saisir le nombre de pièce",
                        ),
                    ],
                    width=6,
                ),
            ],
            className="g-3",
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label([html.Div("Code du type local", id="code-label")], html_for="code"),
                        dcc.Dropdown(
                            id="code",
                            options=[1, 2, 3, 4],
                            searchable= True, placeholder="Veuillez choisir"
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Label("Mois de vente", html_for="mois"),
                        dcc.Dropdown(
                            id="mois",
                            options=[i for i in range(1,13)],
                            searchable= True, placeholder="Veuillez choisir"
                        ),
                    ],
                    width=6,
                ),
            ],
            className="g-3",
        ),

        html.Br(),

        dbc.Col(
            [
                dbc.Label([html.Div("Nombre de lots", id="code-label")], html_for="lot"),
                dcc.Dropdown(
                    id="lot",
                    options=[1, 2, 3, 4, 5],
                    searchable= True, placeholder="Veuillez choisir"
                ),
            ],
            width=12, className="g-3"
        ),

        html.Br(),

        dbc.Toast(
            [html.Div(id='toast_string')], id="toast",
            header="Type local", is_open=False,
            dismissable=True, icon="success", duration= 5000,
            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
        )
    ]
)







#form2------------------------------------------------------------------------------------
form2= html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop ou ',
            html.A('Choisir..', style={}, className="btn btn-primary")
        ]),
        style={
            'width': '95%', 'height': '60px',
            'lineHeight': '60px', 'borderWidth': '1px',
            'borderStyle': 'dashed', 'borderRadius': '5px',
            'textAlign': 'center', 'margin': '5px'
        },
        multiple=False
    ),
    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            dt = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            dt = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' in filename:
            dt= pd.read_table(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            dt.to_dict('records'),
            [{'name': i, 'id': i} for i in dt.columns],
            page_size=10, style_table={'overflowX': 'auto'}, sort_action="native",
            sort_mode="multi"
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])







tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Remplir le formulaire ci-dessous afin de prédire le coût d'un logement!", className="card-text"),
            html.Br(),
            html.Div(children= [form]), 
            dbc.Button("Envoyer", color="primary"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Veuillez Charger une base de données afin de prédire les valeurs foncières!", className="card-text"),
            html.Div(children= [form2]), 
            html.Br(),
            dbc.Button("Envoyer", color="primary"),
        ]
    ),
    className="mt-3",
)


Tab3= dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Prédiction ponctuelle de logement"),
        dbc.Tab(tab2_content, label="Prédiction à grande échelle"),
        html.Br(),
        dbc.Tab(
            "Reformation du modèle", label="Reformation du modèle"
        ),
    ]
)





#call backs --------------------------------------

@callback(
    Output("toast", "is_open"), Output('toast_string', 'children'), Output('code-label', 'children'),
    Input("commune", "value"), Input("departement", "value"), Input("surface", "value"), Input("piece", "value"), 
    Input("code", "value"), Input("mois", "value"), Input("lot", "value"), 
    [State("toast", "is_open")], prevent_initial_call=True
)
def output_text(commune, departement, surface, piece, code, mois, lot, is_open):
    #
    local= None
    if piece is not None and surface is not None:
        url = f"http://api-dash.eu-4.evennode.com/classification/{piece}/{surface}"
        resp = requests.get(url)
        resul= resp.json()
        if "local" in resul.keys():
            local= int(resul["local"])

            return not is_open,   \
                html.P(f"Avec vos spécifications votre type de local est {local}"), \
                html.P(f'Local prédit={local}. Vous pouvez le changer.')
    return is_open, html.P(""), html.P("Code du type local")




@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(content, name, date):
    if content is not None:
        children = parse_contents(content, name, date) 
        return children
