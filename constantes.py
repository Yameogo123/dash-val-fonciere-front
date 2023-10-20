import pandas as pd

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fb",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "25rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


ROW= {
    "display": "flex",
    "flex-direction": "row",
    "justify-content": "space-between",
    "margin": "5px"
}

external_stylesheets = 'https://codepen.io/chriddyp/pen/bWLwgP.css'

df = pd.read_csv('http://api-dash.eu-4.evennode.com/data', low_memory=False, index_col=0)