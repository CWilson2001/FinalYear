from dash import html, callback, Input, Output, dash_table, dcc
from dash.dependencies import Input, Output, State
import time
import pandas as pd
import pathlib
import os

# get relative data folder
PATH = pathlib.Path(__file__).parent

layout = html.Div(children=[
    html.H1(children='Analytics', className="content"),
    html.Button("Check Data Type", id="button_4"),
    html.Div(id='output-data-upload4'),
    html.Br(),
    dcc.Dropdown(
        id='dropdown-columns3',
        options=[],
        value='',
        placeholder='Select a column'
    ),
    html.Br(),
    html.Button("Remove", id="remove-button"),
    html.Div(id='output-remove'),
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
                        incorrect_row_numbers = list(incorrect_rows.index + 2)
                        output.append(f"Not all values in '{col}' are strings")
                        output.append(f"Row numbers with incorrect data type: {incorrect_row_numbers}")
                    elif df[col].str.isnumeric().any():
                        # Get the rows where the data type is incorrect
                        incorrect_rows = df.loc[~df[col].str.isnumeric(), col]
                        incorrect_row_numbers = list(incorrect_rows.index + 2)
                        output.append(f"Not all values in '{col}' are integer")
                        output.append(f"Row numbers with incorrect data type: {incorrect_row_numbers}")
                    else:
                        # Get the rows where the data type is incorrect
                        incorrect_rows = df.loc[~df[col].str.isalpha(), col]
                        incorrect_row_numbers = list(incorrect_rows.index + 2)
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


@callback(Output('output-data-upload4', 'children'),
          State('store', 'data'),
          Input("button_4", "n_clicks"), prevent_initial_call=True)
def update_output4(stored_data, n):
    time.sleep(2)
    children = [
        data_type(stored_data)]
    return children


@callback(Output('dropdown-columns3', 'options'),
          Input('store', 'data'))
def update_output7(stored_data):
    df = pd.read_json(stored_data, orient='split')
    dropdown_options = [{'label': col, 'value': col} for col in df.columns]
    return dropdown_options


@callback(Output('output-remove', 'children'),
          Output('store', 'data'),
          State('dropdown-columns3', 'value'),
          State('store', 'data'),
          Input("remove-button", "n_clicks"), prevent_initial_call=True
          )
def update_output_data(col, content, n):
    df = pd.read_json(content, orient='split')
    output = []

    if col in df.columns:
        if df[col].dtype == 'object':
            if df[col].isnull().any():
                incorrect_rows = df.loc[~df[col].apply(lambda x: isinstance(x, str)), col]
                incorrect_row_numbers = list(incorrect_rows.index)
                df.drop(incorrect_row_numbers, inplace=True)
                output.append("Remove successfully.")
            elif df[col].str.isnumeric().any():
                # Get the rows where the data type is incorrect
                incorrect_rows = df.loc[~df[col].str.isnumeric(), col]
                incorrect_row_numbers = list(incorrect_rows.index)
                df.drop(incorrect_row_numbers, inplace=True)
                df.to_csv(os.path.expanduser("~") + "/Downloads/new.csv", index=False, header=True)
                output.append("Remove successfully222.")

            else:
                # Get the rows where the data type is incorrect
                incorrect_rows = df.loc[~df[col].apply(lambda x: isinstance(x, str)), col]
                incorrect_row_numbers = list(incorrect_rows.index)
                df.drop(incorrect_row_numbers, inplace=True)
                output.append("Remove successfully3333.")
    else:
        output.append("There was an error processing the file")

    return html.Div([html.P(msg) for msg in output]), df.to_json(date_format='iso', orient='split')
