from itertools import count

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from composant import type_objet_connecte as oc
from composant import objets as o
from composant import Lampadaire

colors = {
    'background': 'black',
    'text': '#ffeedd'
}
transparent = go.Layout(
    paper_bgcolor='#121212',
    plot_bgcolor='#121212',
    font={'color': "lightgrey", 'family': "Roboto"},
    margin={"l": 10, "r": 10, "b": 10, "t": 10, "pad": 100},
    height=300,
    width=300,
)

long_graph = go.Layout(
    paper_bgcolor='#121212',
    plot_bgcolor='#121212',
    font={'color': "lightgrey", 'family': "Roboto"},
    margin={"l": 10, "r": 10, "b": 10, "t": 10, "pad": 100},
    yaxis={"range": [0, 100]}
)

# https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/page-2
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#242424",
    "font-family": "Roboto"
}
CONTENT_STYLE = {
    "margin-left": "16rem",
    "padding": "2rem 1rem",
    "background-color": "black",
    "min-height": "100vh"
}

PRIMARY_TEXT = {
    "color": "white",
    "font-size": "48px",
    "font-family": "Roboto",
    "text-align": "center"
}
NAV_LINK = {
    "color": "#dacaba"
}

sidebar = html.Div(
    [
        html.H2("LOGO", className="display-4", style=PRIMARY_TEXT),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Info", href="/page-1",
                            id="page-1-link", style=NAV_LINK),
                dbc.NavLink("Lampadaires", href="/page-2",
                            id="page-2-link", style=NAV_LINK),
                dbc.NavLink("Page 3", href="/page-3",
                            id="page-3-link", style=NAV_LINK),
            ],
            vertical=True,
            pills=True,
        ),
        dcc.Interval(
            id='interval-component',
            interval=0.5*1000,  # ms
            n_intervals=0
        ),
        dcc.Interval(
            id='fast-interval-component',
            interval=0.05*1000,  # ms
            n_intervals=0
        )
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap"],
                meta_tags=[])
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


INFO = html.Div([
    html.H2("Information", style=PRIMARY_TEXT),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Graph(id='live-number-graph'),
        ], className="col-6 d-flex justify-content-center",
           style={'text-align': 'center', 'margin-bottom': '10px'}),
        html.Div([
            dcc.Graph(id='live-type-graph'),
        ], className="col-6 d-flex justify-content-center"),
    ], className="row"),
])

LAMPADAIRE = html.Div([
    html.H2("Lampadaires", style=PRIMARY_TEXT),
    html.Br(), html.Div([
        html.Div([
            dcc.Graph(id='lampadaire-on', animate=True),
        ], className="col-4 d-flex justify-content-center"),
        html.Div([
            dcc.Graph(id='nb-lampadaire'),
        ], className="col-4 d-flex justify-content-center"),
        html.Div([
            dcc.Graph(id='lampadaire-off', animate=True),
        ], className="col-4 d-flex justify-content-center"),
    ], className="row"),
])

cpu_percents = []
ram_percents = []

nums = []
index = count()


@app.callback(Output('live-number-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_number_of_connected_live(n):
    fig = go.Figure(go.Indicator(
        mode="number",
        value=len(oc),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Nombre d'objets"},
    ), layout=transparent)
    return fig


@app.callback(Output('live-type-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    labels = []
    values = []
    labels = list(set(oc))

    for i in labels:
        values.append(oc.count(i))

    labels = [str(i) for i in list(set(oc))]

    fig = go.Figure(
        data=[go.Pie(labels=labels, values=values)], layout=transparent)

    return fig


@app.callback(Output('nb-lampadaire', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_number_of_lampadaire(n):
    value = 0
    for i in o:
        if isinstance(i, Lampadaire):
            value += 1

    fig = go.Figure(go.Indicator(
        mode="number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Nombre de lampadaire"},
    ), layout=transparent)
    return fig


@app.callback(Output('lampadaire-on', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_number_of_lampadaire_on(n):
    value = 0
    total = 0
    for i in o:
        if isinstance(i, Lampadaire):
            total += 1
            if i.est_allume:
                value += 1

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Nombre de lampadaire allumé"},
        gauge={
            'axis': {
                'range': [None, total],
                'tickwidth': 1,
                'tickcolor': "darkblue"
            },
            'bar': {'color': "lightblue"},
        },
    ), layout=transparent)

    return fig


@app.callback(Output('lampadaire-off', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_number_of_lampadaire_off(n):
    value = 0
    total = 0
    for i in o:
        if isinstance(i, Lampadaire):
            total += 1
            if not i.est_allume:
                value += 1

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Nombre de lampadaire allumé"},
        gauge={
            'axis': {
                'range': [None, total],
                'tickwidth': 1,
                'tickcolor': "darkblue"
            },
            'bar': {'color': "lightblue"},
        },

    ), layout=transparent)
    return fig


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return INFO
    elif pathname == "/page-2":
        return LAMPADAIRE
    elif pathname == "/page-3":
        return html.P("Oh cool, this is page 3!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True)
