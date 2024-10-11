from dash import Dash, html, dcc, callback, Output, Input
from data_handler import *
import plotly.express as px
from figure_handler import *


def labelled_graph_callback(app):
    @app.callback(
        Output(component_id="boxplot", component_property="figure"),
        Input(component_id="resolution", component_property="value"),
        Input(component_id="model", component_property="value"),
        Input(component_id="stat", component_property="value")
    )
    def update_graph(resol, model, stat):
        fig = unlabelled_graph(resol, model, stat)

        return fig

def curve_callback(app):
    @app.callback(
        Output(component_id="curveplot", component_property="figure"),
        Input(component_id="curve", component_property="value"),
        Input(component_id="model-labelled", component_property="value"),
        Input(component_id='resolution-labelled', component_property="value")
    )
    def update_curve(curve, model, resol):
        if curve == "Precision-Recall Curve(B)":
            return draw_curve('Precision-Recall(B)', 'Recall', 'Precision', model, resol)
        elif curve == "F1-Confidence Curve(B)":
            return draw_curve('F1-Confidence(B)', 'Confidence', 'F1', model, resol)
        elif curve == "Precision-Confidence Curve(B)":
            return draw_curve('Precision-Confidence(B)', 'Confidence', 'Precision', model, resol)
        elif curve == "Recall-Confidence Curve(B)":
            return draw_curve('Recall-Confidence(B)', 'Confidence', 'Recall', model, resol)

def controls_callback(app):
    @app.callback(
        [Output(component_id='unlabelled_controls', component_property='style'),
        Output(component_id='unlabelled_display', component_property='style'),
        Output(component_id='labelled_controls', component_property='style'),
        Output(component_id='labelled_display', component_property='style')],
        Input(component_id='controls', component_property='value')
    )
    def show_hide_element(visibility_state):
        if visibility_state == 'Unlabelled':
            return (
                {'display': 'block'}, {'display': 'block'},
                {'display': 'none'}, {'display': 'none'})
        if visibility_state == 'Labelled':
            return (
                {'display': 'none'}, {'display': 'none'},
                {'display': 'block'}, {'display': 'block'})

def speed_graph_callback(app):
    @app.callback(
        Output(component_id="speed_graph", component_property="figure"),
        Input(component_id='model-labelled', component_property="value"),
        Input(component_id='resolution-labelled', component_property="value")
    )
    def update_speed_graph(model, res):
        return speed_fig(model, res)

def register_callbacks(app):
    curve_callback(app)
    labelled_graph_callback(app)
    controls_callback(app)
    speed_graph_callback(app)
