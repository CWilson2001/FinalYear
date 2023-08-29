import dash
from dash import html, dcc, callback, Input, Output, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import base64
import datetime
import time
import io
import pandas as pd
from pandas_profiling import ProfileReport
from pathlib import Path
import pathlib
import os
import numpy as np


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
    html.Div(id='output-data-upload'),
    html.Button("Check for Missing and Duplicated Values", id="button_2"),
    html.Div(id='output-data-upload2'),
    html.Button("Generate Report", id="button_4"),
    html.Div(id='output-data-upload3'),
    html.Button("Check Data Type", id="button_3"),
    html.Div(id='output-data-upload4'),
])

layout2 =   html.Div(children=[
            html.H1(children='Analytics', className="content"),
            html.Button("Check for Missing and Duplicated Values", id="button_2"),
            html.Div(id='output-data-upload2'),
        ])

layout3 =   html.Div(children=[
            html.H1(children='Analytics', className="content"),
            html.Button("Check Data Type", id="button_4"),
            html.Div(id='output-data-upload4'),
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


def check_unique(content):
    df = pd.read_json(content, orient='split')
    output = []
    try:
        features_with_na= [features for features in df if df [features].isnull().sum()>0]
        output.append("This is the Percentage for missing data:")
        for feature in features_with_na:
            output.append(f"{feature}:")
            output.append(f"{np.round(df [feature].isnull().mean(),4)*100}%")
        features_with_dup= [features for features in df if df [features].duplicated().sum()]
        features_without_dup= [features for features in df if df [features].duplicated().sum()<50]
        output.append("This is the Percentage for duplicated data:")
        output.append(f"{features_without_dup} do not have duplicated data")
        for feature in features_with_dup:     
            if np.round(df [feature].duplicated().mean(),4)*100 < 50:
                output.append(f"{feature}:")
                output.append(f"{(np.round(df [feature].duplicated().mean(),4)*100)}%")
    except Exception as e:
        print(e)
        return html.Div([
            html.H5("There was an error processing this file.", className='analytics')
        ])
    return html.Div([
        html.Div([html.P(msg) for msg in output]),
        html.Hr(),  # horizontal line
    ])


def report(contents, filename, date):
    global df
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

            profile = ProfileReport(df, title="Pandas Profiling Report")
            assetpath = "./assets/"

            x = 50

            if any(File.endswith('report.html') for File in os.listdir(assetpath)):
                for y in range(x):
                    check = x - y
                    if any(File.startswith(str(check) + "report") for File in os.listdir(assetpath)):
                        check = check + 1
                        reportname = str(check) + "report.html"
                        profile.to_file("./assets/" + reportname)
                        dcc.Link(str(reportname), href="/assets/" + reportname, target="_blank")
            else:
                profile.to_file("./assets/1report.html")

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

            profile = ProfileReport(df, title="Pandas Profiling Report")

            profile.to_file("assets/report.html")
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5("Report has been generated in archive page", className='analytics'),
        html.Hr(),  # horizontal line
    ])


def data_type(content):
    df = pd.read_json(content, orient='split')

    output = []
    try:
        for col in df.columns:
            # Check data type of column
            if df[col].dtype == 'object':
                # Check if all values in column are strings
                if df[col].str.isalpha().all():
                    output.append(f"All values in '{col}' are strings")
                else:
                    if df[col].isnull().any():
                        incorrect_rows = df.loc[~df[col].apply(lambda x: isinstance(x, str)), col]
                        incorrect_row_numbers = list(incorrect_rows.index)
                        output.append(f"Not all values in '{col}' are strings")
                        output.append(f"Row numbers with incorrect data type: {incorrect_row_numbers}")
                    elif df[col].str.isnumeric().any():
                        # Get the rows where the data type is incorrect
                        incorrect_rows = df.loc[~df[col].str.isnumeric(), col]
                        incorrect_row_numbers = list(incorrect_rows.index)
                        output.append(f"Not all values in '{col}' are integer")
                        output.append(f"Row numbers with incorrect data type: {incorrect_row_numbers}")
                    else:
                        # Get the rows where the data type is incorrect
                        incorrect_rows = df.loc[~df[col].apply(lambda x: isinstance(x, str)), col]
                        incorrect_row_numbers = list(incorrect_rows.index)
                        output.append(f"Not all values in '{col}' are strings")
                        output.append(f"Row numbers with incorrect data type: {incorrect_row_numbers}")
            elif df[col].dtype == 'int64':
                # Check if all values in column are integers
                if df[col].apply(lambda x: isinstance(x, int)).all():
                    output.append(f"All values in '{col}' are integers")
                else:
                    # Get the rows where the data type is incorrect
                    incorrect_rows = df.loc[~df[col].apply(lambda x: isinstance(x, int)), col]
                    output.append(f"Not all values in '{col}' are integers")
                    output.append(f"Row numbers with incorrect data type: {incorrect_rows.index.tolist()}")
            elif df[col].dtype == 'float64':
                # Check if all values in column are floats
                if df[col].apply(lambda x: isinstance(x, float)).all():
                    output.append(f"All values in '{col}' are floats")
                else:
                    # Get the rows where the data type is incorrect
                    incorrect_rows = df.loc[~df[col].apply(lambda x: isinstance(x, float)), col]
                    output.append(f"Not all values in '{col}' are floats")
                    output.append(f"Row numbers with incorrect data type: {incorrect_rows.index.tolist()}")
            else:
                # Column has a different data type
                output.append(f"Data type of '{col}' is not object, int64, or float64")

            # Return the output messages as a string
        return html.Div([html.P(msg) for msg in output])
    except Exception as e:
        print(e)
        return html.Div([
            html.H5("There was an error processing this file.", className='analytics')
        ])




# @callback(Output('output-data-upload3', 'children'),
#           State('upload-data', 'contents'),
#           State('upload-data', 'filename'),
#           State('upload-data', 'last_modified'),
#           Input("button_3", "n_clicks"), prevent_initial_call=True)
# def update_output3(list_of_contents, list_of_names, list_of_dates, n):
#     if list_of_contents is not None:
#         time.sleep(2)
#         children = [
#             report(c, n, d) for c, n, d in
#             zip(list_of_contents, list_of_names, list_of_dates)]
#         return children


