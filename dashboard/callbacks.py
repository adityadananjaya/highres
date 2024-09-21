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
        res = filter_results(get_results(), resol, model)

        fig = px.box(res, facet_col="model", y=stat, color="resolution", category_orders={"resolution": [4, 16, 64]}, facet_col_wrap=2)

        dynamic_graph_size(model, fig)

        return fig

def curve_callback(app):
    @app.callback(
        Output(component_id="curveplot", component_property="figure"),
        Input(component_id="curve", component_property="value"),
        Input(component_id="model-labelled", component_property="value")
    )
    def update_curve(curve, model):
        if curve == "Precision-Recall Curve(B)":
            return draw_curve('Precision-Recall(B)', 'Recall', 'Precision', model)
        elif curve == "F1-Confidence Curve(B)":
            return draw_curve('F1-Confidence(B)', 'Confidence', 'F1', model)
        elif curve == "Precision-Confidence Curve(B)":
            return draw_curve('Precision-Confidence(B)', 'Confidence', 'Precision', model)
        elif curve == "Recall-Confidence Curve(B)":
            return draw_curve('Recall-Confidence(B)', 'Confidence', 'Recall', model)

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
        Input(component_id='model-labelled', component_property="value")
    )
    def update_speed_graph(model):
        return speed_fig(model)

def register_callbacks(app):
    curve_callback(app)
    labelled_graph_callback(app)
    controls_callback(app)
    speed_graph_callback(app)
