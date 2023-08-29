from dash import html, callback, Input, Output, dash_table
from dash.dependencies import Input, Output, State
import time
import pandas as pd
import pathlib
import numpy as np
import dash_bootstrap_components as dbc

# get relative data folder
PATH = pathlib.Path(__file__).parent

layout = html.Div(children=[
    html.H1(children='Analytics', className="content"),
    html.Button("Check for Missing and Duplicated Values", id="button_2"),
    html.Div(id='output-data-upload2'),
    html.Div(id='output-data-upload3'),
])


# Checks the percentage of missing/duplicated data within the dataset
def check_unique(content):
    df = pd.read_json(content, orient='split')
    output = []
    try:
        features_with_na = [features for features in df if df[features].isnull().sum() > 0]
        features_without_na = [features for features in df if df[features].isnull().sum() == 0]
        S1 = html.H6("This is the Percentage for missing data:")
        output.append(S1)
        output.append(f"{features_without_na} do not have missing data")
        for feature in features_with_na:
            output.append(f"{feature}:")
            output.append(f"{np.round(df[feature].isnull().mean(), 4) * 100}%")
        features_with_dup = [features for features in df if df[features].duplicated().sum()]
        features_without_dup = [features for features in df if df[features].duplicated().sum() == 0]
        S2 = html.H6("This is the Percentage for duplicated data:")
        output.append(S2)
        output.append(f"{features_without_dup} do not have duplicated data")
        for feature in features_with_dup:
            output.append(f"{feature}:")
            output.append(f"{(np.round(df[feature].duplicated().mean(), 4) * 100)}%")
    except Exception as e:
        print(e)
        return html.Div([
            html.H5("There was an error processing this file.", className='analytics')
        ])
    return html.Div([
        html.Div([html.P(msg) for msg in output]),
        html.Hr(),  # horizontal line
    ])


def remove_unique(content):
    content.dropna(inplace=True)
    content.drop_duplicates(inplace=True)

    return html.Div([
        dash_table.DataTable(
            content.to_dict('records'),
            [{'name': i, 'id': i} for i in content.columns],
            page_size=10
        ),

        html.Hr(),  # horizontal line
    ])


@callback(Output('output-data-upload2', 'children'),
          State('store', 'data'),
          Input("button_2", "n_clicks"), prevent_initial_call=True)
def update_output2(stored_data, n):
    time.sleep(2)
    children = [
        check_unique(stored_data),
        html.Button("Remove Missing/Duplicated Values", id="button_3")]
    return children


@callback(Output('output-data-upload3', 'children'),
          Output('store', 'data', allow_duplicate=True),
          State('store', 'data'),
          Input("button_3", "n_clicks"), prevent_initial_call=True)
def update_output3(stored_data, n):
    df = pd.read_json(stored_data, orient='split')
    time.sleep(2)
    children = [
        remove_unique(df),
        # Next button, links to consistency page
        dbc.Button("Check Consistency", href="http://localhost:8050/apps/consistency", outline=True, color="danger",
                   id="dbc_button")]
    return children, df.to_json(date_format='iso', orient='split')
