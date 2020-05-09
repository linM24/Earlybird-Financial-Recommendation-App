import plotly
from plotly.graph_objs import Candlestick, Layout


def plotly_candle(df):

    data = [
        Candlestick(x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])
    ]

    layout = Layout(
        xaxis_rangeslider_visible=False,
        # paper_bgcolor='rgba(0,0,0,0)',
        # plot_bgcolor='rgba(0,0,0,0)'
    )

    fig = dict(data=data, layout=layout)
    output = plotly.offline.plot(fig, include_plotlyjs=False,
                                 output_type='div')
    return output

if __name__=="__main__":
    plotly_candle()