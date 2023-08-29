from dash import html, callback, Input, Output, dcc
from dash.dependencies import Input, Output, State
import time
import pandas as pd
import pathlib
import plotly.express as px

# get relative data folder
PATH = pathlib.Path(__file__).parent

layout = html.Div(children=[
    html.Button("Pre-defined rules", id="button_5"),
    html.Div(id='output-data-upload6'),
    dcc.Dropdown(
        id='dropdown-columns',
        options=[],
        value='',
        placeholder='Select a column'
    ),
    html.Br(),
    html.Label('Minimum value'),
    dcc.Input(id='input-min', type='number', value=None),
    html.Label('Maximum value'),
    dcc.Input(id='input-max', type='number', value=None),
    html.Button("Check Data Type", id="button"),
    html.Br(),
    html.Div(id='output-data-upload5'),
    html.Br(),
    html.Label('Select a string column to set rule'),
    html.Br(),
    dcc.Dropdown(
        id='dropdown-options',
        options=[],
        value='',
        placeholder='Select a column'
    ),
    html.Label('Check if the value is in the specific column (use coma to input multiple value)(NO SPACING)'),
    html.Br(),
    dcc.Input(
        id='input-value',
        type='text',
        placeholder='Enter a value to check'
    ),
    html.Button('Check', id='check-button'),
    html.Div(id='check-result'),
    html.Br(),
    html.Label('Check if the symbol is contains in the specific column (use coma to input multiple value)(NO SPACING)'),
    html.Br(),
    dcc.Input(
        id='input-symbol',
        type='text',
        placeholder='Enter a value to check'
    ),
    html.Button('Check', id='check-button2'),
    html.Div(id='check-result2')
])


def prerules(content):
    df = pd.read_json(content, orient='split')

    # Define the rules
    rules = {
        'age': {'dtype': 'int64', 'range': [0, 100]},
        'Age': {'dtype': 'int64', 'range': [0, 100]},
        'AGE': {'dtype': 'int64', 'range': [0, 100]},
        'gender': {'dtype': 'object', 'values': ['male', 'female']},
        'Gender': {'dtype': 'object', 'values': ['male', 'female']},
        'GENDER': {'dtype': 'object', 'values': ['male', 'female']},
        'column3': {'dtype': 'float64', 'range': [0.0, 1.0]}
    }

    output = []
    try:
        for col in df.columns:
            # Check if the column is in the rules dictionary
            if col in rules:
                # Check the data type of the column
                if df[col].dtype != rules[col]['dtype']:
                    output.append(f"Error: '{col}' has invalid data type. Expected '{rules[col]['dtype']}'")
                    continue
                # Check the range of values in the column (if applicable)
                if 'range' in rules[col]:
                    min_val, max_val = rules[col]['range']
                    if not df[col].between(min_val, max_val).all():
                        invalid_values = df.loc[~df[col].between(min_val, max_val), col]
                        incorrect_row_numbers = list(invalid_values.index + 2)
                        output.append(
                            f"Error: '{col}' has values outside the range [{min_val}, {max_val}] in following rows: {incorrect_row_numbers}")
                        continue
                    else:
                        output.append(f"Completed: '{col}' has correct value in each row")
                # Check specific values in the column (if applicable)
                if 'values' in rules[col]:
                    valid_values = rules[col]['values']
                    invalid_values = df.loc[~df[col].isin(valid_values), col]
                    incorrect_row_numbers = list(invalid_values.index + 2)
                    if not invalid_values.empty:
                        output.append(
                            f"Error: '{col}' has invalid values in the following rows: {incorrect_row_numbers}")
                        continue
                    else:
                        output.append(f"Completed: '{col}' has correct value in each row")
            else:
                output.append(f"Warning: '{col}' is not defined in the rules")
            # Return the output messages as a string
        output.append("Rule check completed.")
        return html.Div([html.P(msg) for msg in output])
    except Exception as e:
        print(e)
        return html.Div([
            html.H5("There was an error processing this file.", className='analytics')
        ])


@callback(Output('output-data-upload6', 'children'),
          State('store', 'data'),
          Input("button_5", "n_clicks"), prevent_initial_call=True)
def update_output5(stored_data, n):
    time.sleep(2)
    children = [
        prerules(stored_data)]
    return children


@callback(Output('dropdown-columns', 'options'),
          Input('store', 'data'))
def update_output6(stored_data):
    df = pd.read_json(stored_data, orient='split')
    integer_cols = list(df.select_dtypes(include=['int64']).columns)
    dropdown_options = [{'label': col, 'value': col} for col in integer_cols]
    return dropdown_options


@callback(Output('output-data-upload5', 'children'),
          State('dropdown-columns', 'value'),
          State('store', 'data'),
          State('input-min', 'value'),
          State('input-max', 'value'),
          Input("button", "n_clicks"), prevent_initial_call=True
          )
def update_output_data(column, content, min_val, max_val, n):
    df = pd.read_json(content, orient='split')
    output = []

    for col in df.columns:
        if col == column:
            if df[col].between(min_val, max_val).all():
                output.append("Each data is within min and max number")
            else:
                incorrect_rows = df.loc[~df[col].between(min_val, max_val), col]
                incorrect_row_numbers = list(incorrect_rows.index + 2)
                output.append(f"Row numbers with incorrect value: {incorrect_row_numbers}")
        else:
            continue

        return html.Div([html.P(msg) for msg in output])


@callback(Output('dropdown-options', 'options'),
          Input('store', 'data'))
def update_dropdown(stored_data):
    df = pd.read_json(stored_data, orient='split')
    string_cols = list(df.select_dtypes(include=['object']).columns)
    dropdown_options = [{'label': col, 'value': col} for col in string_cols]
    return dropdown_options


@callback(Output('check-result', 'children'),
          State('dropdown-options', 'value'),
          State('store', 'data'),
          State('input-value', 'value'),
          Input("check-button", "n_clicks"), prevent_initial_call=True
          )
def check_value(column, content, value, n, found=None):
    df = pd.read_json(content, orient='split')
    values_list = value.split(',')
    output = []

    if column in df.columns:
        for value in values_list:
            if value in df[column].values:
                output.append(f"Value '{value}' is found in column '{column}'")
            else:
                output.append(f"Value '{value}' not found in column '{column}'")

        incorrect_rows = df.loc[~df[column].isin(values_list), column]
        incorrect_row_numbers = list(incorrect_rows.index + 2)

        for value in values_list:
            output.append(f"Row numbers does not has a value '{values_list}': {incorrect_row_numbers}")
            break

    return html.Div([html.P(msg) for msg in output])


@callback(Output('check-result2', 'children'),
          State('dropdown-options', 'value'),
          State('store', 'data'),
          State('input-symbol', 'value'),
          Input("check-button2", "n_clicks"), prevent_initial_call=True
          )
def check_value(column, content, value, n, found=None):
    df = pd.read_json(content, orient='split')
    values_list = value.split(',')
    output = []

    if column in df.columns:
        for value in values_list:
            if df[column].str.contains(value).any():
                output.append(f"Symbol or character '{value}' is found in column '{column}'")
            else:
                output.append(f"Symbol or character '{value}' is not found in column '{column}'")

        incorrect_rows = df.loc[~df[column].str.contains('|'.join(values_list)), column]
        incorrect_row_numbers = list(incorrect_rows.index + 2)

        for value in values_list:
            output.append(f"Row numbers does not has a value '{values_list}': {incorrect_row_numbers}")
            break

    return html.Div([html.P(msg) for msg in output])
