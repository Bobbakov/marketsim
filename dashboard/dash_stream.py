import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import requests


BASE_ENDPOINT = "http://127.0.0.1:5000/"
ORDER_BOOK_ENDPOINT = BASE_ENDPOINT + "orderbook"


def get_current_orderbook(endpoint):
    current_order_book = requests.get(endpoint).json()
    bids = current_order_book['Bids']
    asks = current_order_book['Asks']
    x = [o[0] for o in bids] + [o[0] for o in asks]
    y = [o[1] for o in bids] + [o[1] for o in asks]
    c = ['Bid' for i in bids] + ['Ask' for i in asks]
    return x, y, c


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)


@app.callback(Output('live-graph', 'figure'),
              Input('graph-update', 'n_intervals'))
def update_graph_scatter(n):
    X, Y, c = get_current_orderbook(ORDER_BOOK_ENDPOINT)
    title = 'LOB'
    fig = px.scatter(x=list(X),
                     y=list(Y),
                     color=c,
                     title=title)
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
    fig.update_xaxes(title_text='Price')
    fig.update_yaxes(title_text='Quantity')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)