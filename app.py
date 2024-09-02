from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

results_4mp = pd.read_csv('results/4mpresults.csv')
results_16mp = pd.read_csv('results/16mpresults.csv')
results = pd.concat([results_16mp, results_4mp])
external_stylesheets = [dbc.themes.FLATLY]

app = Dash(__name__, external_stylesheets=external_stylesheets)


fig = px.box(results, x="model", y="detections", color="resolution")

controls = dbc.Card([
    html.Div([
        "Resolution",
        dcc.Dropdown(
            options=[
                {'label': '4 MP Images', 'value':'4'},
                {'label': '16 MP Images', 'value':'16'}
            ],
            value='4', 
            id='resolution', 
            multi=True
        )
    ]),
    html.Div([
        "Model",
        dcc.Dropdown(
            options=[
                {'label': 'YOLOv8 Extra Large', 'value':'extra_large'},
                {'label': 'YOLOv8 Large', 'value':'large'},
                {'label': 'YOLOv8 Medium', 'value':'medium'},
                {'label': 'YOLOv8 Small', 'value':'small'},
                {'label': 'YOLOv8 Nano', 'value':'nano'}
            ],
            value=['extra_large', 'nano'],
            id='model',
            multi=True
        )
    ]),
    html.Div([
        'Statistic',
        dcc.Dropdown(
            options=[
                {'label': 'Number of Detections', 'value': 'detections'},
                {'label': 'Average Confidence', 'value': 'average confidence'}
            ],
            value='detections',
            id='stat'
        )
    ]),
], body=True, style={'margin-top': '50px'})

app.layout = dbc.Container([
    dbc.Row([
        html.H1(children='High-res vs Low-res Images for Boat Detection', style={'textAlign':'center'}),
        html.Hr()
    ]),
    dbc.Row([
        dbc.Col(controls, width=4),
        dbc.Col([
            dcc.Graph(figure = {}, id='boxplot')
        ], width=8)
    ])
], fluid=True)

@callback(
    Output(component_id="boxplot", component_property="figure"),
    Input(component_id="resolution", component_property="value"),
    Input(component_id="model", component_property="value"),
    Input(component_id="stat", component_property="value")
)
def update_graph(resol, model, stat):
    res = results
    if(type(resol) is str):
        res = results[results.resolution == int(resol)]
    else:
        res = results[results.resolution.isin([eval(i) for i in resol])]

    if(type(model) is str):
        res = res[res.model == model]
    else:
        res = res[res.model.isin(model)]
    
    fig = px.box(res, x="model", y=stat, color="resolution")

    return fig

if __name__ == '__main__':
    app.run(debug=True)
