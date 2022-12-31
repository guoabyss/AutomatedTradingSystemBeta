import time
import numpy as np
import pandas
import pandas as pd
import mplfinance as mpf
from config import resample_period, resample_map


class CandleDataGraph(object):
    """数据k线图"""

    def initial_fetch(self, q_data_list: list):
        """
        init dataframe, init data length >= 100
        :param q_data_list:
        :return:
        """
        df = pd.DataFrame
        for q_data in q_data_list:
            _df = self._data_clean_(q_data)
            if df.empty:
                df = _df
            else:
                df = pd.concat([df, _df])
        return df

    @staticmethod
    def plot(data_frame):
        data_frame.index = pd.DatetimeIndex(data_frame.index)
        rs = data_frame.resample(resample_period).agg(resample_map).dropna()
        fig, axes = mpf.plot(rs, returnfig=True, type='candle', figsize=(11, 8), title='\n\nOkx')
        ax = axes[0]
        return fig, ax

    def fetch_next(self, q_data):
        return self._data_clean_(q_data)

    @staticmethod
    def _data_clean_(q_data):
        """
        数据清洗
        :return: dataframe
        """
        data_list = q_data[0]
        data_dict = {
            'Open': float(data_list[1]),
            'High': float(data_list[2]),
            'Low': float(data_list[3]),
            'Close': float(data_list[4]),
            'Volume': float(data_list[7]),
        }
        index_list = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data_list[0]) / 1000))]
        df = pandas.DataFrame(data=data_dict, index=index_list)
        return df


cdg = CandleDataGraph()


