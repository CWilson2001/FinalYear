from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import webbrowser
from threading import Timer

# Main file
from app import app
from app import server

# App pages
from apps import home
from apps import report
from apps import upload
from apps import missing_duplicated
from apps import consistency
from apps import rules
from apps import visual

# Static Sidebar for application
sidebar = html.Div(
    [
        html.Div(
            [
                html.H2("Menu"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),

        # Links for pages
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("Home")],
                    href="/apps/home",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"),
                        html.Span("Upload Dataset"),
                    ],
                    href="/apps/upload",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"),
                        html.Span("Uniqueness & Completeness"),
                    ],
                    href="/apps/unique",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"),
                        html.Span("Consistency"),
                    ],
                    href="/apps/consistency",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"),
                        html.Span("Rules"),
                    ],
                    href="/apps/rules",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"),
                        html.Span("Visualisation"),
                    ],
                    href="/apps/visual",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"),
                        html.Span("Report"),
                    ],
                    href="/apps/report",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)


# Function that opens a browser that leads to the web application
def open_browser():
    webbrowser.open_new("http://localhost:{}".format(8050))


# Function that returns the layout of the application
def server_layout():
    return dbc.Container(
        [
            dcc.Location(id='url', refresh=True),

            # Stores data for the session, will be kept until browser/tab is closed
            dcc.Store(id='store', storage_type='session'),

            # # Stores data locally, will be kept until browser's cache is cleared
            # dcc.Store(id='store', storage_type='local'),

            dbc.Row(
                (  # Sidebar location in layout
                    dbc.Col(
                        (
                            sidebar
                        ), xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
                    # Main body and page content in layout
                    dbc.Col(
                        (
                            dbc.Row(
                                html.Div("Data Quality Requirement and Readiness Assessment Tool"),
                                style={'fontSize': 50, 'textAlign': 'center'},
                            ),
                            html.Hr(),
                            dbc.Row(
                                html.Div(id='page_content', children=[])
                            ),
                        ), xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
                )
            )
        ], fluid=True
    )


# Layout of the application
app.layout = server_layout


# Callback that links all the additional pages' layout to this page.
@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/home':
        return home.layout
    if pathname == '/apps/upload':
        return upload.layout
    if pathname == '/apps/unique':
        return missing_duplicated.layout
    if pathname == '/apps/consistency':
        return consistency.layout
    if pathname == '/apps/report':
        return report.layout
    if pathname == '/apps/rules':
        return rules.layout
    if pathname == '/apps/visual':
        return visual.layout
    else:
        return home.layout


# Running the application
if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=False, host='0.0.0.0', port=8050)
