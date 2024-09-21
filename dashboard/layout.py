from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from callbacks import *

controls = dbc.Card([
    html.Div([
        "Metrics",
        dcc.RadioItems(
            options=['Unlabelled', 'Labelled'],
            value='Unlabelled',
            id='controls'
        )
    ]),
    html.Div([
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
    ], id='unlabelled_controls', style= {'display': 'block'}),
    html.Div([
        html.Div([
            "Curve",
            dcc.Dropdown(
                options=[
                    {'label': 'Precision-Recall Curve(B)', 'value':'Precision-Recall Curve(B)'},
                    {'label': 'F1-Confidence Curve(B)', 'value':'F1-Confidence Curve(B)'},
                    {'label': 'Precision-Confidence Curve(B)', 'value':'Precision-Confidence Curve(B)'},
                    {'label': 'Recall-Confidence Curve(B)', 'value':'Recall-Confidence Curve(B)'}
                ],
                value='Precision-Recall Curve(B)',
                id='curve'
            )
        ]),
        html.Div([
            "Resolution",
            dcc.Dropdown(
                options=[
                    {'label': '16 MP Images', 'value':'16'}
                ],
                value=['16'], 
                id='resolution-labelled', 
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
                id='model-labelled',
                multi=True
            )
        ])
    ], id='labelled_controls', style= {'display': 'block'})
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
        ], width=8, id='unlabelled_display', style= {'display': 'block'}),
        dbc.Col([
            dcc.Graph(figure = {}, id='curveplot')
        ], width=8, id='labelled_display', style= {'display': 'block'})

    ]),
], fluid=True)