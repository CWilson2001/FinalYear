from dash import html, dcc, callback, Input, Output, clientside_callback
import dash_bootstrap_components as dbc
import pathlib
import os
import visdcc

# Get relative data folder
PATH = pathlib.Path(__file__).parent
assetpath = os.listdir("./assets/")

# Function to update the asset path for generated reports
def update_path(a):
    a = os.listdir("./assets/")
    return a

# Function to generate links for reports
def generate_link(b):
    if b.endswith("report.html"):
        return dbc.Row(dcc.Link(str(b), href="/assets/" + b, target="_blank", id="report-link"))

# Function to show the links in the layout
def generate_layout(c):
    return dbc.Row([
        dbc.Col(children=[generate_link(i) for i in c], id="report"),
    ])

# Layout of the Archive page (Added at "page_content")
layout = html.Div([
    html.Div(children=[
    html.H1(children='Archive'),
    html.Div(id="report_links"),
    # Original button
    # html.Div([
    #     html.Button("Download", id="click1"),
    #         visdcc.Run_js(id = 'javascript')
    # ]),
    # Interval every 1000 milliseconds 
    dcc.Interval(
        id="interval_component",
        interval=1 * 1000,
        n_intervals=0
    )
], id="print"),
    dbc.Button(children=['Download'],className="mr-1",id='js',n_clicks=0),], id='main')

clientside_callback(
    """
    function(n_clicks){
        if(n_clicks > 0){
            var opt = {
                margin: 1,
                filename: 'myfile.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 3},
                jsPDF: { unit: 'cm', format: 'a2', orientation: 'p' },
                pagebreak: { mode: ['avoid-all'] }
            };
            html2pdf().from(document.getElementById("print")).set(opt).save();
        }
    }
    """,
    Output('js','n_clicks'),
    Input('js','n_clicks')
)

# Callback to refresh the page per the interval given
@callback(Output("report_links", 'children'),
          Input("interval_component", "n_intervals"))
def update_links(n):
    new_asset = update_path(assetpath)
    return generate_layout(new_asset)

# Use the CTRL + P
# @callback(Output("javascript", 'run'),
#           Input("click1", "n_clicks"))
# def download_func(n):
#     if n:
#         return "window.print()"
