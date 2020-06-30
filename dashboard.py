import datetime

import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import plotly
import plotly.graph_objects as go
import plotly.subplots
import plotly.express as px
from dash.dependencies import Input, Output

from composant import type_objet_connecte as oc
from composant import objets as o
from composant import Intersection, FeuCirculation, Lampadaire

colors = {
    'background': '#dddddd',
    'text': '#7FDBFF'
}
transparent = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H1('Info',
                style={
                    'fontSize': 48,
                    'textAlign': 'center',
                    'color': colors['text']
                }
                ),
        html.Div([
            html.Div([
                dcc.Graph(id='live-number-graph'),
            ], className="six columns"),
            html.Div([
                dcc.Graph(id='live-type-graph'),
            ], className="six columns"),
        ], className="row"),
        dcc.Dropdown(
            id='opt-dropdown',
             style={'width': '80%', 'display': 'inline-block'}
        ),
        html.Div(id='display-selected-values'),
        dcc.Interval(
            id='interval-component',
            interval=0.5*1000,  # in milliseconds
            n_intervals=0
        )],
        style = {
            "backgroundColor": colors['background']
        }))


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


@app.callback(
    Output('opt-dropdown', 'options'),
    [Input('interval-component', 'n_intervals')]
)
def update_date_dropdown(name):
    # [{'label': 'a', 'value': 'a'}]
    try:
        r = [{'label': str(i), 'value': str(inx)} for inx, i in enumerate(o)]
        return r
    except Exception as e:
        print(e)
        return [{'label': 'a', 'value': 'a'}]

@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('opt-dropdown', 'value')])
def set_display_children(selected_value):
    inx = int(selected_value)
    obj = o[inx]
    if isinstance(obj, Intersection):
        return f'Intersection id({obj.ids})'

    elif isinstance(obj, FeuCirculation):
        return f'Feu de Circulation id({obj.ids}) {obj.etat}'

    elif isinstance(obj, Lampadaire):
        return f'Lampadaire id({obj.ids}) {obj.est_allume}'

if __name__ == '__main__':
    app.run_server(debug=True)
