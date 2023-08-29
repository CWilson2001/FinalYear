from dash import html, callback, Input, Output, dcc
from dash.dependencies import Input, Output, State
import time
import pandas as pd
import pathlib
import plotly.express as px

# get relative data folder
PATH = pathlib.Path(__file__).parent

layout = html.Div(children=[
    dcc.Dropdown(
        id='dropdown-columns2',
        options=[],
        value='',
        placeholder='Select a column'
    ),
    dcc.Dropdown(
        id='dropdown-distributions',
        options=[
            {'label': 'Histogram', 'value': 'histogram'},
            {'label': 'Box', 'value': 'box'},
            {'label': 'Violin', 'value': 'violin'}
        ],
        value='histogram',
        placeholder='Select a distribution type'
    ),
    dcc.Graph(id='graph')
])


@callback([Output('dropdown-columns2', 'options'),
           Output('dropdown-columns2', 'value')],
          [Input('store', 'data')])
def update_dropdown(contents):
    df = pd.read_json(contents, orient='split')
    if df is not None:
        options = [{'label': col, 'value': col} for col in df.columns]
        return options, options[0]['value']
    else:
        return [], ''


@callback(Output('graph', 'figure'),
          [Input('dropdown-columns2', 'value'),
           Input('dropdown-distributions', 'value')],
          [State('store', 'data')])
def update_graph(column, distribution, contents):
    global fig
    time.sleep(1)
    df = pd.read_json(contents, orient='split')
    if df is not None:
        if column in df.columns:
            if distribution == 'histogram':
                fig = px.histogram(df, x=column, nbins=10)
            elif distribution == 'box':
                fig = px.box(df, y=column)
            elif distribution == 'violin':
                fig = px.violin(df, y=column)
            return fig
    return {}