import dash
import dash_bootstrap_components as dbc

# Meta tags for mobile responsive app layout
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.SPACELAB]
                )

# Server for the application
server = app.server