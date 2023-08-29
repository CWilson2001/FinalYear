import dash
from dash import html, dcc, Input, Output, callback
import pathlib
import dash_bootstrap_components as dbc

from apps import analytics

# get relative data folder
PATH = pathlib.Path(__file__).parent

# Layout of Home Page (Added at "page_content")
layout = html.Div([
    html.Div([
        html.H5("Why is data quality important?", className='home'),
        html.P("Improved data quality leads to a better overall analysis of specific datasets. In other words:", className='home'),
        html.P("Improving the quality of data helps companies to make more accurate and informed decisions.", id="bolded", className='home'),
        html.P("Hence, data cleaning is one of the most important steps in data analysis.", className='home'),

        # Get started button, links to upload page
        html.Div(id='startbutton'),
        dbc.Button("Get Started", href="http://localhost:8050/apps/upload", outline=True, color="danger", id="dbc_button"),
        html.P("Click on the get GET STARTED button above to start your dataset quality assessment", className='home'),
        html.H5("Disclaimer:", className='home'),
        html.P("This program is to be used as a supplement to data cleaning and for data quality assessment. The datasets uploaded may still need to be manually cleaned before usage.", className='home'),

        # Image from assets folder
        html.Img(src=dash.get_asset_url('INFOGRAPHIC.png'), className="center", alt="Data Cleaning Checklist")
    ])
])