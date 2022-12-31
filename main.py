import mplfinance as mpf
from config import data_Q, OkxPublicTopic, apikey, secretkey, resample_period, resample_map
from tradeView.showTrade import cdg
import matplotlib.animation as animation
from tradeData.websocket_okx import PublicChannel
from threading import Thread
import pandas as pd

animate_df = pd.DataFrame


def ws_okx():
    pub_ws = PublicChannel(OkxPublicTopic, apikey, secretkey)
    pub_ws.tickers()
    pub_ws.run()


def run_trade():
    trade_data_list = []
    initial_trade_df = None
    while True:
        trade_data = data_Q.get()
        if len(trade_data_list) < 1:
            if int(trade_data[0][-1]) == 1:
                trade_data_list.append(trade_data)
        else:
            if not initial_trade_df:
                initial_trade_df = cdg.initial_fetch(trade_data_list)
                break
    fig, ax = cdg.plot(initial_trade_df)
    ani = animation.FuncAnimation(fig, animate, fargs=(initial_trade_df, ax), interval=250)
    mpf.show()


def animate(*args):
    global animate_df
    initial_trade_df = args[1]
    ax = args[2]
    q_data = data_Q.get()
    next_data = cdg.fetch_next(q_data)
    if animate_df.empty:
        animate_df = pd.concat([initial_trade_df, next_data])
    else:
        animate_df = pd.concat([animate_df, next_data])
    animate_df.index = pd.DatetimeIndex(animate_df.index)
    rs = animate_df.resample(resample_period).agg(resample_map).dropna()
    print(rs)
    ax.clear()
    mpf.plot(rs, ax=ax, type='candle')


if __name__ == '__main__':
    t1 = Thread(target=ws_okx)
    t2 = Thread(target=run_trade)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
