from dash import Dash, html, dcc, dash_table
import pandas as pd

dico= {
    "No disposition":["int64", "pas de valeurs manquantes"], "Code commune":["int64", "pas de valeurs manquantes"], "No plan":["int64", "pas de valeurs manquantes"], 
    "Nombre de lots":["int64", "pas de valeurs manquantes"], "No voie":["float64", "valeurs manquantes inférieures à 45%"], "Code postal":["float64", "valeurs manquantes inférieures à 0%"],
    "Prefixe de section":["float64", "valeurs manquantes supérieur à 95%"], "4eme lot":["float64", "valeurs manquantes supérieures à 90%"], "Code type local":["float64", "valeurs manquantes inférieures à 40%"],
    "Surface reelle bati":["float64", "valeurs manquantes inférieures à 45%"], "Nombre pieces principales":["float64", "valeurs manquantes inférieures à 40%"],
    "Surface terrain":["float64", "valeurs manquantes inférieures à 45%"], "Date mutation":["object", "pas de valeurs manquantes"], "Nature mutation":["object", "pas de valeurs manquantes"],
    "Valeur fonciere":["object", "1% de valeurs nan"], "B/T/Q":["object", "valeurs manquantes supérieur à 65%"], "Type de voie":["object", "valeurs manquantes inférieures à 45%"],
    "Code voie":["object","valeurs manquantes inférieur à 0%"], "Voie":["object", "valeurs manquantes inférieures à 0%"], "Commune":["object", "pas de valeurs manquantes"],
    "Code departement":["object", "pas de valeurs manquantes"], "Section":["object", "pas de valeur manquantes"], "No Volume":["object", "valeurs manquantes supérieures à 99%"],
    "1er lot":["object", "valeurs manquantes supérieures à 65%"], "Surface Carrez du 1er lot":["object", "valeurs manquantes supérieures à 90%"], "2eme lot":["object", "valeurs manquantes supérieures à 90%"],
    "3eme lot":["object", "valeurs manquantes supérieures à 90%"], "Surface Carrez du 2eme lot":["object", "valeurs manquantes supérieures à 90%"], "5eme lot":["object", "valeurs manquantes supérieures à 90%"],
    "Type local":["object", "valeurs manquantes inférieures à 40%"], "Surface Carrez du 3eme lot":["object", "valeurs manquantes supérieures à 90%"],
    "Nature culture":["object", "valeurs manquantes inférieures à 40%"], "Nature culture speciale":["object", "valeurs manquantes supérieures à 95%"]
}

image_path = 'assets/classif.png'

df= pd.DataFrame.from_dict(dico)

Tab1= html.Div(className='control-tab', children=[
        html.H1(className='Introduction', children=[html.P("Prédiction des valeurs foncières")]),
        html.Br(),
        html.H2(className="topic", children=[html.P("I- Le thème")]),
        html.Br(),
        html.Div("Les valeurs foncières des habitations en France nous sont données sur une période de 4 ans \
        s'étendant de 2018 à 2021 inclu. Ces valeurs foncières qui prennent en compte les appartements, dépendances, maisons et zones industrielles \
        sont repertoriées dans 4 bases de données différentes dépendant de l'années. Ces bases de données contiennent des informations sur le type de \
        logement, la situation géographique (communes, départements, code postal, ...), les caractéristiques de ces logements (superficie, nombres de pièces) \
        Chaque base contient des millions d'individus (ici, ce sont les logements). "),
        html.Div("Il nous est demandé de créer un modèle de prédiction de la valeur foncière en passant par une classification de valeurs manquantes sur le \
        type du local. "),

        html.Br(),
        html.Br(),
        html.H2(className="approche", children=[html.P("II- Une approche")]),
        html.Br(),
        html.Div("L'exploitation des données brutes afin de tirer la bonne information de toutes nos données a été la première de nos préoccupations."),
        html.Br(),
        html.H4("1- L'analyse univariée"),
        html.Br(),
        dcc.Markdown('''
            Chaque base de données contenait plus de **3 millions** pour **43 variables**.
            Les préréquis à l'analyse sont la transformation de valeur de la variable cible (Valeur fonciere) en float (type numéric), et la concaténation de nos 4 bases.
            Parmis nos variables, certaines (indicatrices) étaient toutes **nulles**. Il s'agit notamment de:
            - Identifiant de document
            - Reference document
            - Tous les Articles CGI
                     
            **Action: Sans trop refléchir, on se débarasse de ces colonnes qui nous apportent aucunes informations.**
        
        '''),
        html.Div("Par la suite on s'est intéressé à la proportion de valeurs nulles. Soit le tableau suivant:"),
        html.Br(),
        dash_table.DataTable(   
            data=df.to_dict('records'), page_size=10, style_table={'overflowX': 'auto'}, sort_action="native",
            sort_mode="multi"
        ),
        html.Br(),
        dcc.Markdown('''
            Les colonnes ayant plus de **65%** de valeurs nulles ont été supprimées.
            Il s'agit entre autres de:
            - Prefixe de section
            - tous les lots et surface carrez de lot
            - Nature culture speciale
            - B/T/Q
                     
            **Remarques: Les lignes ayant des valeurs manquantes pour la valeur foncière ont été supprimées car cette dernière est notre variable cible.**
            
            Par contre les autres variables ont vu leurs valeurs nulles être imputés différentes façon. En particulier un modèle de classification supervisé sur le type
            du local a été mené afin d'estimer (supposer) les futures valeurs nulles de nos données à prédire.
                     
        '''),
        html.Br(),
        dcc.Markdown('''
            Des successions de croisement de tableaux ont permis de connaitre et identifier des colonnes en doubles (l'un étant une forme encodée de l'autre)
            Il s'agit de:
            - Type local et Code type local
            - Code voie et Voie
            - Code departement et Departement
            - Code commune et Commune
            **Autres remarques: Ces colonnes en double ont été laissée tombée (pas toutes mais une par paire).**
        '''),
        
        html.Br(),
        html.H4("2- L'analyse bivariée"),
        html.Br(),
        dcc.Markdown('''
            La corrélation des variables quantitatives, (que nous avons mis sur le github) nous montre que la valeur \
            foncière n'est pas en grande relation avec les autres variables. Ce qui nous a poussé à aller chercher des données \
            d'autres sources notamment: 
            - De INSEE sur la longitute-latitude des communes
            - De INSEE sur le prix au m2 par commune
            - De .... sur le niveau de vie par commune
            Comme attendu, il y'a une grande corrélation entre les deux dernières et la valeur foncière.

            **NB**: En ce qui concerne la classification, le type du local a bien une relation (correlation) avec le nombre de pièces principales et la surface du terrain
        '''),
        html.Br(),

        dcc.Markdown('''
            Une classification non supervisé (CAH) de variables nous a permis de voir les variables qui semblaient apporter la même information.
            **NB**: Celà a influencé nos choix pour former nos modèles.
        '''),

        html.Img(src=image_path, style={'height':'90%','width':'70%'}),

        html.Br(),

        dcc.Markdown('''
            Des boxplots ont été effectué ce qui nous a permis de détecter les valeurs abbhérentes. Ces valeurs ont été rétirés. Ainsi que les individus ayant des valeurs foncières spéciales (0, 1)
            ou très grandes ou très petites. (Ils ont été supprimé par la méthode IQR afin de ne pas biaiser le modèle). 
            Aussi, dépendant du type de logement, les valeurs foncières avaient des écart très important. Un problème de variance se posait également.
        '''),

        html.Br(),
        html.Br(),
        html.H2(className="proposition", children=[html.P("III- Notre proposition")]),
        html.Br(),

        dcc.Markdown('''
            Après avoir testé plusieurs algorithmes de régression (linéaire et ses pénalités, SVM, arbre, RF), optimisé les paramètres de ces algorithmes (avec grid search et CV),
            Fais une sélection de variables (intuitivement, lasso, ...) nous en sommes venu à la conclusion suivante:
            Il serait "mieux" de faire la prédiction de chaque type de logement: c'est à dire faire des modèle adapté à chaque type.
            
            - Il est mis à disposition une application dash communiquant avec 
            - une API fastapi pour gérer la partie classification du type de local et l'estimation des prix.
            - Un github avec tous les notebooks de synthèse.
                     
            Veuillez trouver les liens ci-bas.
            
        '''),

        html.Br(),
        html.Br(),
        html.H2(className="propos", children=[html.P("IV- A propos")]),
        html.Br(),

        dcc.Markdown('''
            Sous la supervision de M. Sardellitti, ce projet de machine learning a été réalisé par 4 élèves du Master SISE:
            - Cyrielle ()
            - Nathan (https://github.com/Naghan1132)
            - Joseph ()
            - Wendyam ()
                     
            Lien github de notre travail : https://github.com/Naghan1132/Property_price_prediction/tree/main
                     
            Les liens API:
                - route principales: adresse= http:
                - classification unitaire (get) : adresse + /classification/(le nombre de pièce)/(la surface du terrain)
                - classification sur un fichier (post): adresse + /classification (avec un envoi du fichier en csv ou txt)
                - Idem pour la prédiction en remplaçant classification par regression dans la route.
        '''),

        html.Br(),
        html.Br()
        
    ]
)