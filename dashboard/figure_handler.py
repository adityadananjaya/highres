import plotly.express as px
from data_handler import *
from math import floor
from dash import Dash, dash_table
import pandas as pd

def unlabelled_graph(resol, model, stat):
    res = filter_results(get_results(), resol, model)

    fig = px.box(
            res, 
            facet_col="model", 
            y=stat, 
            color="resolution", 
            category_orders={"resolution": ['4', '16', '64']}, 
            facet_col_wrap=2
        )

    dynamic_graph_size(model, fig)

    return fig

def draw_curve(curve, x, y, model, resol):
    results = get_labeled_results()
    curves = results[1]

    curves = filter_results(curves, resol, model)

    curves_filter = curves[curves["curve"] == curve]
    curves_filter.loc[:,x] = curves_filter[x].apply(lambda x_: x_[0] if isinstance(x_, list) and len(x_) > 0 and isinstance(x_[0], list) else x_)
    curves_filter.loc[:,y] = curves_filter[y].apply(lambda x_: x_[0] if isinstance(x_, list) and len(x_) > 0 and isinstance(x_[0], list) else x_)
    curves_exploded = curves_filter.explode([x, y])

    fig = px.line(
        curves_exploded, 
        x=x, 
        y=y, 
        line_dash='resolution',
        color="model",
        labels={x: x, y: y},
        title=curve,
        height = 750
    )

    fig.update_layout(
        font=dict(
            family="Times New Roman",
            size=20
        ))

    return fig

def filter_results(res, resol, model):
    if(type(resol) is str):
        res = res[res.resolution == resol]
    else:
        res = res[res.resolution.isin(resol)]
    
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
            for i in metrics.columns]
    )

# Resolution # Model # AUC #

def AUC_table(model, res, curve):
    results = get_labeled_results()
    metrics = filter_results(results[1], res, model)
    curve_ = curve.split()[0] + "(B)"
    metrics = metrics[metrics.curve == curve_]
    AUCs = metrics[["resolution", "model", "AUC"]]
    return AUCs.to_dict('records'), [{'id': c, 'name': c} for c in AUCs.columns]

def speed_fig(model, res):
    results = get_labeled_results()
    metrics = filter_results(results[0], res, model)

    speed = metrics[["model", "resolution", "Time Taken"]]
    speed_long = pd.melt(speed, id_vars=["model", "resolution"], value_vars= ['Time Taken'])

    fig = px.bar(speed_long, x="model", y="value", color="resolution", title="Model Speeds", barmode="group",
            labels={'value': 'Time Taken (s)', 'variable': 'Process'})
    return fig