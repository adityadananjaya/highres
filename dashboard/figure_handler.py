import plotly.express as px
from data_handler import *
from math import floor

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
        height=750
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