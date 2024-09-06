from dash import Dash, html, dcc, callback, Output, Input
from data_handler import *
import plotly.express as px
from math import floor

def filter_results(res, resol, model):
    if(type(resol) is str):
        res = res[res.resolution == int(resol)]
    else:
        res = res[res.resolution.isin([eval(i) for i in resol])]
    
    if(type(model) is str):
        res = res[res.model == model]
    else:
        res = res[res.model.isin(model)]

    return res

def dynamic_graph_size(model, fig):
    mult = floor(len(model) / 2.5) + 1 if len(model) > 1 else 1
    
    fig.update_layout(
        height=500*mult,
    )

def register_callbacks(app):
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
