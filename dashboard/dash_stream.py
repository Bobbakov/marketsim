import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots

import plotly.graph_objs as go
import requests
import pandas as pd


BASE_ENDPOINT = "http://127.0.0.1:5000/"
ORDER_BOOK_ENDPOINT = BASE_ENDPOINT + "orderbook"
TRADES_ENDPOINT = BASE_ENDPOINT + 'trades'


def get_current_orderbook(endpoint):
    current_order_book = requests.get(endpoint).json()
    return current_order_book


def get_trades(endpoint):
    trades = requests.get(endpoint).json()
    return trades


def json_to_trades(trades_json):
    cols = ['TradeID', 'TradeTime', 'Price', 'Qty', 'BuyerMaker']
    trades = (pd.DataFrame(trades_json['Trades'], columns=cols)
              .assign(TradeTime=lambda x: pd.to_datetime(x['TradeTime']))
              )
    return trades


def orderbook_to_vertical(orderbook_json):
    # give bids negative rank for plot
    bids = (pd.DataFrame(orderbook_json['Bids'], columns=['Price', 'Quantity'])
            .assign(Quantity=lambda x: x['Quantity'],
                    Color='Green',
                    id=lambda x: x.index,
                    Rank=lambda x: -x.groupby('Price')['id'].rank('first')))

    asks = (pd.DataFrame(orderbook_json['Asks'], columns=['Price', 'Quantity'])
            .assign(Color='Red',
                    id=lambda x: x.index,
                    Rank=lambda x: x.groupby('Price')['id'].rank('first')))
    df = pd.concat([bids, asks]).sort_values('Price')
    x = list(df['Rank'])
    y = list(df['Price'])
    c = list(df['Color'])
    q = list(df['Quantity'])
    return x, y, c, q


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
            .sort_values(0, ascending=False))
    bids_price = list(bids[0])
    bids_qty = list(bids[1].cumsum())

    asks = (pd.DataFrame(orderbook_json['Asks'])
            .groupby(0)
            .sum()
            .reset_index()
            .sort_values(0))
    asks_price = list(asks[0])
    asks_qty = list(asks[1].cumsum())

    y = bids_qty + asks_qty
    x = bids_price + asks_price
    c = ['Green' for i in bids_price] + ['Red' for i in asks_price]

    return x, y, c


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
    x_density, y_density, c_density = orderbook_to_density(orderbook)
    x_vertical_lob, y_vertical_lob, c_vertical_lob, quantity_vertical_lob = orderbook_to_vertical(orderbook)

    trades_json = get_trades(TRADES_ENDPOINT)
    trades = json_to_trades(trades_json)

    x_price = list(trades['TradeTime'])
    y_price = list(trades['Price'])
    # sort descending for trades display
    trades = trades.sort_values('TradeTime', ascending=False)

    fig = make_subplots(rows=2,
                        cols=2,
                        subplot_titles=("Price", "CLOB", "CLOB - Density", 'Trades'),
                        # row_heights=[0.15, 0.55, 0.15, 0.15],
                        specs=[[{"type": "scatter"}, {"type": "scatter"}],
                               [{"type": "scatter"}, {"type": "table"}]]
                        )

    # add price chart
    row_1 = 1
    col_1 = 1
    fig.append_trace(go.Scatter(x=x_price,
                                y=y_price,
                                mode='lines+markers'
                                ),
                     row=row_1,
                     col=col_1)
    fig.update_xaxes(row=row_1, col=col_1, range=[x_price[0]-pd.Timedelta(seconds=3), x_price[-1]+pd.Timedelta(seconds=1)])

    # add clob
    row_2 = 1
    col_2 = 2
    fig.append_trace(go.Scatter(y=y_vertical_lob,
                                x=x_vertical_lob,
                                text=quantity_vertical_lob,
                                # orientation='h',
                                marker={'color': c_vertical_lob},
                                mode='markers+text',
                                textposition="top center"),
                     row=row_2,
                     col=col_2)
    # fig.update_traces(row=2, col=1, mode='markers', marker_line_width=1, marker_size=10, marker_line_color='white')
    fig.update_xaxes(row=row_2, col=col_2, title_text='Quantity')
    fig.update_yaxes(row=row_2, col=col_2, title_text='Price')

    # add density orderbook
    row_3 = 2
    col_3 = 1
    fig.append_trace(go.Scatter(x=list(x_density),
                                y=list(y_density),
                                marker={'color': c_density},
                                ),
                     row=row_3,
                     col=1)
    fig.update_traces(row=row_3, col=col_3, mode='markers', marker_line_width=1, marker_size=10, marker_line_color='white')
    fig.update_xaxes(row=row_3, col=col_3, title_text='Price')
    fig.update_yaxes(row=row_3, col=col_3, title_text='Quantity')

    # add transactions
    row_4 = 2
    col_4 = 2
    fig.append_trace(go.Table(header=dict(values=trades.columns),
                              cells=dict(values=[list(trades[trades.columns[0]]),
                                                 list(trades[trades.columns[1]]),
                                                 list(trades[trades.columns[2]]),
                                                 list(trades[trades.columns[3]]),
                                                 list(trades[trades.columns[4]])
                                                 ])),
                     row=row_4,
                     col=col_4)

    fig.update_layout(height=1200, showlegend=False,
                      template='plotly_dark'
                      )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)