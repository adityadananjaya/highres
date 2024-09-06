from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import *
from data_handler import *
external_stylesheets = [dbc.themes.FLATLY]

app = Dash(__name__, external_stylesheets=external_stylesheets)

fig = px.box(get_results(), x="model", y="detections", color="resolution")

register_callbacks(app)

app.layout = layout

if __name__ == '__main__':
    app.run(debug=True)