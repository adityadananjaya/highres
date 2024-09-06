from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

controls = dbc.Card([
    html.Div([
        "Resolution",
        dcc.Dropdown(
            options=[
                {'label': '4 MP Images', 'value':'4'},
                {'label': '16 MP Images', 'value':'16'},
                {'label': '64 MP Images', 'value':'64'}
            ],
            value=['4', '16'], 
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


layout = dbc.Container([
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