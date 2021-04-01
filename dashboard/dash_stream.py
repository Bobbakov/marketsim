import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots

import plotly.graph_objs as go
import requests
import numpy as np
import pandas as pd


BASE_ENDPOINT = "http://127.0.0.1:5000/"
ORDER_BOOK_ENDPOINT = BASE_ENDPOINT + "orderbook"


def get_current_orderbook(endpoint):
    current_order_book = requests.get(endpoint).json()
    return current_order_book


def orderbook_to_scatter(orderbook_json):
    bids = orderbook_json['Bids']
    asks = orderbook_json['Asks']
    x = [o[0] for o in bids] + [o[0] for o in asks]
    y = [o[1] for o in bids] + [o[1] for o in asks]
    c = ['Green' for i in bids] + ['Red' for i in asks]
    return x, y, c


def orderbook_to_density(orderbook_json):
    bids = (pd.DataFrame(orderbook_json['Bids'])
            .groupby(0)
            .sum()
            .reset_index()
            .sort_values(0, ascending=False)
            )
    bids_price = list(bids[0])
    bids_qty = list(bids[1].cumsum())

    asks = (pd.DataFrame(orderbook_json['Asks'])
            .groupby(0)
            .sum()
            .reset_index()
            .sort_values(0)
            )
    asks_price = list(asks[0])
    asks_qty = list(asks[1].cumsum())

    y = bids_qty + asks_qty
    x = bids_price + asks_price

    return x, y


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000)
    ]
)


@app.callback(Output('live-graph', 'figure'),
              Input('graph-update', 'n_intervals'))
def update_graph_scatter(n):

    orderbook = get_current_orderbook(ORDER_BOOK_ENDPOINT)
    x_scatter, y_scatter, c_scatter = orderbook_to_scatter(orderbook)
    x_density, y_density = orderbook_to_density(orderbook)

    title = 'LOB'

    fig = make_subplots(rows=2,
                        cols=1,
                        subplot_titles=("LOB - Scatter", "LOB - Density")
                        )

    fig.append_trace(go.Scatter(x=x_scatter,
                                y=y_scatter,
                                marker={'color': c_scatter}
                                ),
                     row=1,
                     col=1
                     )
    fig.append_trace(go.Scatter(x=list(x_density),
                                y=list(y_density)),
                     row=2,
                     col=1
                     )

    fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
    fig.update_xaxes(title_text='Price')
    fig.update_yaxes(title_text='Quantity')
    fig.update_layout(height=700, showlegend=False)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)