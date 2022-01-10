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

    def curr_price(self, tick = "BTCUSDT"):
        order = {}
        order["symbol"] = tick
        resp = requests.request("GET", base + "api/v3/avgPrice", params = order)
        print(resp.json())
        return round(float(resp.json()["price"]),2)
    def hist_new(self, tick = "BTCUSDT", tr = '1d'):
        order = {}
        old = "api/v3/klines"
        points = {"1d": ["1m", np.timedelta64(1, 'D')],
                "1w": ["1h", np.timedelta64(7, 'D')],
                "1m": ["4h", np.timedelta64(30, 'D')],
                "3m": ["6h", np.timedelta64(90, 'D')],
                "1y": ["1w", np.timedelta64(365, 'D')],
                "3y": ["1w", np.timedelta64(1095, 'D')]
                }
        order["symbol"] = tick
        order["interval"] = points[tr][0]
        now = np.datetime64("now")
        order["startTime"] = str(self.to_ms(now-points[tr][1]))
        order["endTime"] = str(self.to_ms(now))
        resp = requests.request("GET", base + old, params= order)
        his = pd.DataFrame(resp.json(), columns=["opentime", "open", "high", "low", "close", "volume", "closetime", "qav", "ntrades", "tbav", "tqav", "ig"])
        his = his.astype(float)
        his["timestamps"] = pd.date_range(now-points[tr][1], now, len(his))
        return his
    
    def all_ticks(self):
        resp = requests.request("GET", base + "api/v3/exchangeInfo")
        return resp.json()
    
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

app = dash.Dash(external_stylesheets=[dbc.themes.YETI, "https://codepen.io/chriddyp/pen/bWLwgP.css", "https://www.herokucdn.com/purple3/latest/purple3.min.css"])
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
                    dcc.Input(placeholder="Search by Tick...", value="BTCUSDT", id="search", size="8")
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
                        value='high',
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
                            {'label': '1 Year', 'value': '1y'},
                            {'label': '3 Years', 'value': '3y'}
                        ],
                        value='1d',
                        id='times'
                    )
                ],
                title="Time Range"
                ),

            ],
            flush=True),
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
            dbc.Container(
        [
            html.H1("Live Value Counter", className="display-3"),
            html.H2("Tick here",
                className="lead",
                id="jtron"
            ),
            html.Hr(className="my-2"),
            html.P("Refreshed Cryptovalue", id="cval"),
            dcc.Interval(interval=30000, n_intervals=0, id="internal-component")
        ],
        fluid=True,
        className="py-3",
        )
        ],
        width={"offset":2}),
        dbc.Col([
            html.H1("Similar Crypto", className='display-3'),
            html.Hr(className='my-2'),
            html.P("Coming Soon!")
        ],
        className="h-100 p-5 text-white border bg-dark rounded-3"),

    ]),
    dbc.Row(html.P("Made by Christopher Pak, 2022"))
])

@app.callback(
    [Output("mainplot", "figure"),
    Output("volplot", "figure"),
    Output("jtron", "children")],
    [Input("search", "value"),
    Input("ddohlc", "value"),
    Input("times", "value")]
)
def update_figs(query, opt, interval):
    cp = Crypto()
    new_df = cp.hist_new(query.upper(), interval)
    fig1 = px.line(new_df, x="timestamps", y=opt, title= (query + " Price Timeline"))
    fig2 = px.bar(new_df,x="timestamps",y="volume", title=(query + " Volume"))
    return fig1, fig2, query
@app.callback(
    Output("cval", "children"),
    [Input("internal-component", "n_intervals"),
    Input('search', 'value')]
)
def live_price(n, query):
    cp = Crypto()
    curr_price = cp.curr_price(tick=query)
    return curr_price

if __name__ == "__main__":
    app.run_server(debug=True)