from dash import html, dcc, callback, Input, Output, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import base64
import io
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc

# get relative data folder
PATH = pathlib.Path(__file__).parent

layout = html.Div(children=[
    html.H1(children='Analytics', className="content"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
    ),
    html.Div(
        [
            html.H5("Timeliness & Accuracy of Data"),
            html.P("Before uploading, make sure the dataset is:"),
            html.P("1. Accurate & Relevant"),
            html.P("""  The information within the dataset should be sufficient to fulfill a given task. 
                        The information should also be correct to prevent untrue or incorrect analysis results. 
                        E.g. If a customer has deleted their account and their account is still within the current accounts dataset, 
                        that dataset is not accurate or relevant
                        """),
            html.P("2. Timely"),
            html.P("""  The dataset should be as up-to-date as possible to increase the viability and reliability of the analysis. 
                        E.g. If you have a dataset with information on customers from 2008, and another with information on customers from 2021, 
                        upload the more recent version.
                        """),
        ], id='output-data-upload')
])


def parse_contents(content):
    df = pd.read_json(content, orient='split')
    return html.Div([
        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            page_size=10
        ),

        html.Hr(),  # horizontal line
    ])


@callback(Output('store', 'data', allow_duplicate=True),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'),
          prevent_initial_call=True)
def store_data(list_of_contents, list_of_names):
    if list_of_contents is None:
        raise PreventUpdate

    content_type, content_string = list_of_contents.split(',')

    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in list_of_names:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in list_of_names:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            html.H5("There was an error processing this file.", className='analytics')
        ])

    return df.to_json(date_format='iso', orient='split')


@callback(Output('output-data-upload', 'children'),
          Input('store', 'data'))
def update_output(stored_data):
    children = [parse_contents(stored_data),
                # Next button, links to upload page
                dbc.Button("Check Uniqueness and Completeness", href="http://localhost:8050/apps/unique", outline=True,
                           color="danger", id="dbc_button"), ]
    return children
