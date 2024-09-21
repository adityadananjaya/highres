import plotly.express as px
from data_handler import *
from math import floor
from dash import Dash, dash_table
import pandas as pd


def draw_curve(curve, x, y, model):
    results = get_labeled_results()
    curves = results[1]

    if(type(model) is str):
        curves = curves[curves.model == model]
    else:
        curves = curves[curves.model.isin(model)]

    curves_filter = curves[curves["curve"] == curve]
    curves_filter.loc[:,x] = curves_filter[x].apply(lambda x_: x_[0] if isinstance(x_, list) and len(x_) > 0 and isinstance(x_[0], list) else x_)
    curves_filter.loc[:,y] = curves_filter[y].apply(lambda x_: x_[0] if isinstance(x_, list) and len(x_) > 0 and isinstance(x_[0], list) else x_)
    curves_exploded = curves_filter.explode([x, y])

    fig = px.line(
    curves_exploded, 
        x=x, 
        y=y, 
        color='model', 
        labels={x: x, y: y},
        title='Precision-Recall Curve',
        height=600,
    )
    return fig

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


def get_table(columns):
    results = get_labeled_results()
    metrics = results[0]
    metrics = metrics[columns]
    
    return dash_table.DataTable(
        data=metrics.to_dict('records'), 
        columns=[
            {"name": i, 
            "id": i,
            "type": "numeric",
            "format": { "specifier": ".3f"}} 
            for i in metrics.columns])

def speed_fig(model):
    results = get_labeled_results()
    metrics = results[0]
    
    if(type(model) is str):
        metrics = metrics[metrics.Model == model]
    else:
        metrics = metrics[metrics.Model.isin(model)]

    speed = metrics[["Model", "preprocess", "inference", "loss", "postprocess"]]
    speed_long = pd.melt(speed, id_vars="Model", value_vars= ['preprocess', 'inference', 'loss', 'postprocess'])

    fig = px.bar(speed_long, x="Model", y="value", color="variable", title="Model Speeds",
            labels={'value': 'Speed (ms)', 'variable': 'Process'})
    return fig
