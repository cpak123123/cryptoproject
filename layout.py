from dash import html, dcc
from dash import Input, Output
import plotly.express as px
import dash
from api import Crypto
#For Base layout
colors = {"background": '#005C5C',
        "text": '#B5E847'}
app = dash.Dash(__name__)
cp = Crypto()
dlt = cp.hist_new()    
fig = px.line(dlt, x = "timestamps", y = "open", title = "Opening dates")
fig.update_layout({
    'plot_bgcolor': 'rgba(153,221,124,0.8)',
    'paper_bgcolor': 'rgba(123,190,94,0.8)'
})
home_lay = html.Div(
    children = [
    html.H1(
        children= "Binance Crypto Visualization",
        style={
            'text_align': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children = [
        dcc.Graph(
        id='test-graph',
        figure=fig
        ),
        html.Br(),
        html.Label("Variety"),
        dcc.Checklist(
            id = 'cl',
            options = [
                {'label': 'Open', 'value': 'open'},
                {'label': 'Close', 'value': 'close'},
                {'label': 'High', 'value': 'high'}
            ]
        ),
        html.Br(),
        html.Div(
            id='out',
        )
    ]    
    )
])

@app.callback(
    Output(component_id='out', component_property='children'),
    Input(component_id='cl', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value) 

fore_lay = html.Div(
    children = [html.H2("Forecasting Done here")]
)