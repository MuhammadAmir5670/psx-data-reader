from psx import stocks, tickers
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import datetime


tickers = tickers()

data = stocks("EFERT", start=datetime.date(2010, 1, 1), end=datetime.date.today())

fig = go.Figure()

fig = make_subplots(rows=1, cols=1)

fig = make_subplots(rows=2,
                    cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=('EFERT', 'Volume'),
                    row_width=[0.3, 0.7])



fig.append_trace(
    go.Candlestick(
        x=data.index,
        open=data.Open,
        high=data.High,
        low=data.Low,
        close=data.Close,  
    ), row=1, col=1
)
fig.add_trace(
    go.Bar(x=data.index,
           y=data.Volume,
           marker_color="green",
           showlegend=False),
    row=2,
    col=1
)
# volume_bar = go.Figure()

fig.update_layout(title="EFERT Stocks",
                  yaxis_title="Price (PKR)",
                  width=1400,
                  height=700)

fig.update(layout_xaxis_rangeslider_visible=False)
fig.show()

