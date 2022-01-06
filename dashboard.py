import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.express as px
"""
|API, REQUESTS, AND DATA RELATED STUFF|
"""
class Crypto:
    global base
    global test
    base = "https://api.binance.com/"
    test = "api/v3/time"
    def __init__(self):
        # print(requests.request("GET", base+test))
        pass
    def current_sym(self, ticks):
        exchange = "api/v3/exchangeInfo?symbol="
        resp = requests.request("GET", base + exchange + ticks)
        return resp.json()

        #update: please use klines api to get hist data :)
    def hist(self, tick = "BTCUSDT", backlog = 5):
        old = "api/v3/trades"
        symbol = "?symbol=" + tick
        limit = "limit=" + str(backlog)
        st = "start"
        resp = requests.request("GET", base + old + symbol + "&" + limit)
        return resp.json()

    def hist_new(self, tick = "BTCUSDT", interval = '1d',  st = np.datetime64("now") - np.timedelta64(30, 'D'), et = np.datetime64("now")):
        order = {}
        old = "api/v3/klines"
        order["symbol"] = tick
        order["interval"] = interval
        order["startTime"] = str(self.to_ms(st))
        order["endTime"] = str(self.to_ms(et))
        resp = requests.request("GET", base + old, params= order)
        his = pd.DataFrame(resp.json(), columns=["opentime", "open", "high", "low", "close", "volume", "closetime", "qav", "ntrades", "tbav", "tqav", "ig"])
        his = his.astype(float)
        his["timestamps"] = pd.date_range(st, et, len(his))
        return his
    
    def to_ts(self, ms):
        target_dt = np.datetime64("1970-01-01") + np.timedelta64(ms, 'ms')
        return target_dt

    def to_ms(self, ts):
        ms = ts.astype(np.int64)*1000
        return ms

"""
|DASHBOARD THINGS|
"""
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(external_stylesheets=[dbc.themes.YETI, "https://codepen.io/chriddyp/pen/bWLwgP.css"])
cp = Crypto()
df = cp.hist_new()

app.layout=html.Div([
    dbc.Row(
        html.H1("CryptoCurrency Dashboard")
    ),
    dbc.Row([
        dbc.Col(
            dbc.Accordion([
                dbc.AccordionItem([
                    dcc.Input(placeholder="Search by Tick...", value=""),
                    html.Button("Search")
                ],
                title="Search"),
                dbc.AccordionItem([
                    dcc.Dropdown(
                        options=[
                            {'label': 'Open', 'value': 'open'},
                            {'label': 'High', 'value': 'high'},
                            {'label': 'Low', 'value': 'low'},
                            {'label': 'Close', 'value': 'close'},
                            {'label': 'Volume', 'value': 'volume'}
                        ],
                        value='High',
                        id='ddohlc'
                    )
                ],
                title="Chart Details"
                ),
                dbc.AccordionItem([
                    dcc.RadioItems(
                        options=[
                            {'label': '1 Day', 'value': '1d'},
                            {'label': '1 Week', 'value': '1w'},
                            {'label': '1 Month', 'value': '1m'},
                            {'label': '3 Months', 'value': '3m'},
                            {'label': '1 Year', 'value': '1y'}
                        ],
                        value='1 Month',
                        id='times'
                    )
                ],
                title="Time Range"
                ),

            ]),
            width=2
        ),
        dbc.Col(
                dcc.Graph(id = 'mainplot',
                    figure = px.line(df, x = "timestamps", y = "high", title = "Opening dates")),
                width=5
        ),
        dbc.Col(
                dcc.Graph(id = 'volplot',
                    figure = px.bar(df, x = "timestamps", y = "volume", title = "Volume")),
                width=5
        )
    ]),
    dbc.Row([
        dbc.Col([
            html.H1("Today's Statistics", className='display-3'),
            html.Hr(className='my-2'),
            html.P("High: "+ "Low: "+ "Open: "+ "Close: ")
        ],
        className="h-100 p-5 text-white border bg-dark rounded-3",
        width={"offset":2}),
        
    ]),
    dbc.Row(html.P("Made by Christopher Pak, 2022"))
])

if __name__ == "__main__":
    app.run_server(debug=True)