from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
from callbacks import *
from figure_handler import *

unlabelled_controls = html.Div([
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
    ], id='unlabelled_controls', style= {'display': 'block'})

labelled_controls = html.Div([
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
                    {'label': '4 MP Images', 'value': '4'},
                    {'label': '16 MP Images', 'value':'16'},
                    {'label': '64 MP Images', 'value':'64'}
                ],
                value=['4', '16'], 
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
                value=['extra_large', 'medium', 'nano'],
                id='model-labelled',
                multi=True
            )
        ]),
        html.Div([
            dbc.Col([
                dash_table.DataTable(
                    id='AUCtable',
                    data=[],
                    columns=[]
                )
            ])
        ])
    ], id='labelled_controls', style= {'display': 'block'})

AUC_table_layout = html.Div(
    dbc.Accordion([
        dbc.AccordionItem([
            html.Div([
                dbc.Col([
                    dash_table.DataTable(
                        id='AUCtable',
                        data=[],
                        columns=[]
                    ),
                ])
            ])
        ], title="Area Under Curve (AUC) Table"),
        dbc.AccordionItem([
            html.Div([
                dbc.Col([
                    dcc.Graph(figure={}, id="speed_graph")
                ]
                )
            ])
        ], title="Model Processing Speeds")
    ], start_collapsed=True)
)

speed_graph_layout = html.Div(
    dbc.Accordion
)

controls = dbc.Card([
    html.Div([
        "Metrics",
        dcc.RadioItems(
            options=['Unlabelled', 'Labelled'],
            value='Labelled',
            id='controls'
        )
    ]),
    unlabelled_controls,
    labelled_controls
], body=True, style={'margin-top': '50px'})

labelled_display = dbc.Col([
    dcc.Graph(figure = {}, id='boxplot')], 
    width=8, id='unlabelled_display', 
    style= {'display': 'block'}
)

unlabelled_display = dbc.Col([
    dcc.Tabs([
        dcc.Tab(label='Curves', children=[
            dbc.Col([
                dcc.Graph(figure = {}, id='curveplot')
            ])
        ]),
        dcc.Tab(label='Metrics', children=[
            dbc.Col([
                get_table(["model", "resolution", "Precision", "Recall", "mAP50", "mAP50-95", "Fitness"])],
                id="metric_table",
            )
        ])
    ])
], 
    width=8, 
    id='labelled_display', 
    style= {'display': 'block'}
)


layout = dbc.Container([
    dbc.Row([
        html.H1(children='High-res vs Low-res Images for Boat Detection', style={'textAlign':'center'}),
        html.Hr()
    ]),
    dbc.Row([
        dbc.Col([controls, AUC_table_layout], width=4),
        labelled_display,
        unlabelled_display
    ]),
], fluid=True)