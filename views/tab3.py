from dash import html, dcc, callback, Output, Input, dash_table, State, ctx
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
                        dbc.Label("Surface bati", html_for="surface_bati"),
                        dbc.Input(
                            type="number", id="surface_bati",
                            placeholder="Veuillez saisir la surface", min=0
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
                        dbc.Label("Surface réelle du terrain", html_for="surface"),
                        dbc.Input(
                            type="number", id="surface",
                            placeholder="Veuillez saisir..", min=0
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Label("Nombre pièces principales", html_for="piece"),
                        dbc.Input(
                            type="number", id="piece",
                            placeholder="Veuillez saisir le nombre de pièce", min= 0
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
                        dbc.Label([html.Div("Date de mutation", id="annee")], html_for="annee"),
                        dbc.Input(
                            type="date", id="annee",
                            placeholder="Veuillez saisir", size="lg",
                            className="form-control"
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Label("Le code postal", html_for="poste"),
                        dbc.Input(
                            type="text", id="poste",
                            placeholder="Veuillez saisir..", value="62990", required= True
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
                            searchable= True, placeholder="Veuillez choisir (ou laisser vide)"
                        ),
                    ],
                    width=6,
                )
            ],
            className="g-3",
        ),

        html.Br(),

        dbc.Toast(
            [html.Div(id='toast_string')], id="toast",
            header="Type local", is_open=False,
            dismissable=True, icon="success", duration= 5000,
            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Votre valeur foncière en euro est de :")),
                dbc.ModalBody("chargement.....", id="md-body"),
                # dbc.ModalFooter(
                #     dbc.Button(
                #         "Close", id="close", className="ms-auto", n_clicks=0
                #     )
                # ),
            ],
            id="modal",
            is_open=False,
        ),
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
        multiple=False, max_size=-1
    ),
    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    files = {'database': (filename, decoded), 'filename': filename}
    r = requests.post('http://api-dash.eu-4.evennode.com/regression', files=files)
    resultats= r.json()

    if 'prediction' in resultats:
        res=resultats["prediction"]
    else:
        res= [{"error": "Votre fichier n'a pas les spécifications nécessaire pour une prédiction. Désolé!"}]

    tab= pd.DataFrame.from_records(res)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            dt = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            dt = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' in filename:
            dt= pd.read_table(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        return html.Div([
            'Erreur de chargement du fichier'
        ])

    return html.Div([
        html.H5(f"le fichier que vous venez de charger est {filename} ({datetime.datetime.fromtimestamp(date)})"),

        dash_table.DataTable(
            dt.to_dict('records'),
            [{'name': i, 'id': i} for i in dt.columns],
            page_size=10, style_table={'overflowX': 'auto'}, sort_action="native",
            sort_mode="multi"
        ),

        html.Hr(),

        html.H5(f"les prédictions des valeurs foncières de votre fichier sont: "),

        dash_table.DataTable(
            tab.to_dict('records'),
            [{'name': i, 'id': i} for i in tab.columns],
            page_size=10, style_table={'overflowX': 'auto'}, sort_action="native",
            sort_mode="multi", export_format="csv",
        ),

        html.Hr(),  # horizontal line

        # # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])




#----------------------------------- REFORMATION DU MODELE




accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    html.P("Veuillez choisir les modèles sur lesquels vous comptez refaire la régression"),
                    html.Br(),
                    dcc.Dropdown(
                        id="c_model",
                        options=["lasso", "ridge", "svm linéaire", "arbre de décision", "forêt aléatoire"],
                        searchable= True, placeholder="Faites vos choix", multi= True
                    ),
                ],
                title="MODELE",
            ),
            dbc.AccordionItem(
                [
                    html.P("Choisir les prétraitements que vous aimeriez appliquer"),
                    html.Br(),
                    dcc.Dropdown(
                        id="c_pretraitement",
                        options=["drop na > 50%", "standardiser les quantitatifs", "Normaliser les quantitatifs", "Encoder les qualitatifs par label", "Encoder les qualitatifs par onehot"],
                        searchable= True, placeholder="Faites vos choix", multi= True
                    )
                ],
                title="PRETRAITEMENT",
            ),
            dbc.AccordionItem(
                [
                    html.P("Choisir les colonnes que vous aimeriez ignorer"),
                    html.Br(),
                    dcc.Dropdown(
                        id="c_ignore",
                        options=list(df.columns),
                        searchable= True, placeholder="Faites vos choix", multi= True
                    ),
                    html.Br(),
                ],
                title="REDUCTIONS VARIABLES",
            ),

            dbc.AccordionItem(
                [
                    html.P("Choisir la réduction que vous aimeriez appliquer"),
                    html.Br(),
                    dcc.Dropdown(
                        id="c_dimension",
                        options=["ACP", "ACM", "AFDM", "select k best"],
                        searchable= True, placeholder="Faites vos choix", multi= False
                    ),
                    html.Br(),
                ],
                title="REDUCTION DIMENSION",
            ), 

            dbc.AccordionItem(
                [
                    html.P("Choisir une nouvelle base de données à ajouter aux anciennes"),
                    html.Label("Choisir une base de petite taille"),
                    html.Br(),
                    dcc.Upload(
                        id='c_donnees',
                        children=html.Div([
                            'glisser déposé ou ',
                            html.A('Choisir..', style={}, className="btn btn-primary")
                        ]),
                        style={
                            'width': '95%', 'height': '60px',
                            'lineHeight': '60px', 'borderWidth': '1px',
                            'borderStyle': 'dashed', 'borderRadius': '5px',
                            'textAlign': 'center', 'margin': '5px'
                        },
                        multiple=False, max_size=-1
                    ),
                    html.Br(),
                ],
                title="BASE DE DONNÉES",
            ),
        ],
        # always_open=True
    ),

)






#------------------------------------- FORMATIONS DE NOS TABS QUI FONT APPELS AUX HTML CI DESSUS

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Remplir le formulaire ci-dessous afin de prédire le coût d'un logement!", className="card-text"),
            html.Br(),
            html.Div(children= [form]), 
            dbc.Button("Envoyer", color="primary", id="pred", disabled= True),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Veuillez charger une base de données afin de prédire les valeurs foncières!", className="card-text"),
            html.P("veuillez choisir un fichier pas volumineux please!", className="card-text"),
            html.Div(children= [form2]), 
            html.Br()
        ]
    ),
    className="mt-3",
)


tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Reformation du modèle", className="card-text"),
            html.Label("Nous tenons à préciser que pour des limites de capacité le lancement du nouveau modèle ne passe pas", className="card-text danger"),
            html.Br(),
            accordion, 
            html.Br(),
            dbc.Button("Former", color="primary", id="form", disabled= True),
            html.Br(),
            html.Div(id="results")
        ]
    ),
    className="mt-3",
)



#---------------- REGROUPEMENT DE NOS TABS

Tab3= dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Prédiction ponctuelle de logement"),
        dbc.Tab(tab2_content, label="Prédiction à grande échelle"),
        html.Br(),
        dbc.Tab(tab3_content, label="Reformation du modèle"),
    ]
)





#call backs --------------------------------------

@callback(
    Output('pred', 'children'), Output("modal", "is_open"), Output("md-body", "children"),
    Output('code-label', 'children'), Output('pred', 'disabled'),
    Input("commune", "value"), Input("surface_bati", "value"), Input("surface", "value"), 
    Input("piece", "value"), Input("code", "value"), Input("annee", "value"),
    Input("poste", "value"), [Input('pred','n_clicks')],
    [State("toast", "is_open")], prevent_initial_call=True
)
def output_text(commune, surface_bati, surface, piece, code, annee, poste, is_open, n_clicks):
    #
    mess= "Code du type local"
    if None not in [piece, surface, surface_bati, commune, annee, poste]:
        date= "/".join(annee.split("-")[::-1])
        #Classification
        url_classif = f"http://api-dash.eu-4.evennode.com/classification/{piece}/{surface}/{surface_bati}"
        resp_class = requests.get(url_classif)
        resul_classif= resp_class.json()
        
        if "local" in resul_classif.keys():
            local= int(resul_classif["local"])
            mess= f'Local prédit={local}. Vous pouvez le changer.'

        body={
            "Nombre_pieces_principales": int(piece), 
            "Surface_reelle_bati": surface_bati,
            #"Code_type_local": code,
            "Surface_terrain": float(surface),
            "Date_mutation": date,
            "Commune": commune,
            "Code_postal": poste
        }

        url = f"http://api-dash.eu-4.evennode.com/regression/simple"

        prix= "--"

        if ctx.triggered_id == "pred":
            if code is None:
                body["Code_type_local"]= local
            else:
                body["Code_type_local"]= int(code)
            resp = requests.post(url, json=body)
            resul= resp.json()
            if 'prediction' in resul.keys():
                prix= str(round(resul['prediction'][0]["TARGET"], 2))

            #[dbc.Spinner(size="sm"), " Loading..."],
            return  html.P("Envoyer"), True, html.P(prix), html.P(mess), False
        
        return html.P("Envoyer"), False, html.P(prix), html.P(mess), False
    
    return html.P("Envoyer"), False, html.P("loading"), html.P(mess), True
    

@callback(Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'))
def update_output(content, name, date):
    if content is not None:
        children = parse_contents(content, name, date) 
        return children


@callback(Output("results", "children"), Output("form", "disabled"),
    Input('c_model', "value"),        
    Input('c_pretraitement', "value"),        
    Input('c_ignore', "value"),        
    Input('c_dimension', "value"),        
    Input('c_donnees', "contents"),    
    State('c_donnees', 'filename')    
)
def reformation(model, pretraitement, ignore, dimension, donnee, filename):

    if None not in [model, pretraitement, ignore, dimension, donnee]:
        content_type, content_string = donnee.split(',')

        decoded = base64.b64decode(content_string)
        files = {'database': (filename, decoded), 'filename': filename}
        #{"filename": filename, "filedata": decoded}

        form= {
            "model": model,
            "pretraitement": pretraitement,
            "ignore": ignore,
            "dimension": dimension
        }

        #r = requests.post('http://api-dash.eu-4.evennode.com/reformation', data={"reformation": form, "database": {"filename": filename, "filedata": decoded}}, headers={"Content-Type":'application/x-www-form-urlencoded'})
        #resultats= r.json()
        #print(resultats)


        return html.P("merci votre demande a été reçu et sera traité dans les plus bref délai"), False
    return None, True
