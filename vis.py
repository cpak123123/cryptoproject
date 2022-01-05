import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from layout import *
import callbacks
from api import Crypto

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

cp = Crypto()
dlt = cp.hist_new()    
fig = px.line(dlt, x = "timestamps", y = "open", title = "Opening dates")

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Crypto Dashboard"),
        
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Input(
                placeholder="Search for Crypto Tickers...",
                type='text',
                value=''
            ),
            dbc.Button("click me"),
            dcc.Graph(
                id='test-graph',
                figure=fig
            )
        ])
    ])

])


if __name__ == "__main__":
    app.run_server(debug=True)