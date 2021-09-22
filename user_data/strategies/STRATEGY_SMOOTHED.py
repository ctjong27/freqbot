# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy.interface import IStrategy

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

_total_length = 500

class STRATEGY_SMOOTHED(IStrategy):
    """
    Strategy SMOOTHED
    author@: Fractate_Dev
    github@: https://github.com/Fractate/freqbot
    How to use it?
    > python3 ./freqtrade/main.py -s SMOOTHED
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "60": 0.01,
        "30": 0.02,
        "0": 0.04
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.10

    # Trailing stoploss
    trailing_stop = False

    # Optimal timeframe for the strategy.
    timeframe = '5m'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 20

    # Optional order type mapping.
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }

        # 'subplots': {
        #     # Subplots - each dict defines one additional plot
        #     "MACD": {
        #         'macd': {'color': 'blue'},
        #         'macdsignal': {'color': 'orange'},
        #     },
        #     "RSI": {
        #         'rsi': {'color': 'red'},
        #     }
        # }
    plot_config = {
        # Main plot indicators (Moving averages, ...)
        'main_plot': {
            'ema10': {},
            'ema10smoothed': {},
            'ema_smoothed_goingup': {},
            'wt_goingup':{},
        },
        'subplots': {
            # Subplots - each dict defines one additional plot
            "WaveTrend": {
                'wt1': {'color': 'blue'},
                'wt2': {'color': 'orange'},
                '0' : {},
                '-70' : {},
                '-80' : {},
                '70' : {},
                '80' : {},
            },
        }
    }
    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """

        # Getting Smooth EMA
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=_total_length)
        # dataframe['ema10smoothed'] = (dataframe['ema10'] + dataframe['ema10'].shift(1) + dataframe['ema10'].shift(2) + dataframe['ema10'].shift(3) + dataframe['ema10'].shift(4) + dataframe['ema10'].shift(5)) / 6
        dataframe['ema10smoothed'] = 0
        for i in range(_total_length):
            dataframe['ema10smoothed'] += dataframe['ema10'].shift(i)/_total_length

        # Getting Wavetrend
        # ap = hlc3 
        # esa = ema(ap, n1)
        # d = ema(abs(ap - esa), n1)
        # ci = (ap - esa) / (0.015 * d)
        # tci = ema(ci, n2)

        # wt1 = tci
        # wt2 = sma(wt1,4)

        # freqtrade plot-dataframe -c CONFIG.json -s STRATEGY_SMOOTHED --timeframe 30m -p BAT/BTC --timerange=20200601-20200715
        dataframe['ap'] = dataframe["close"] + dataframe["high"] + dataframe["low"]
        dataframe['esa'] = ta.EMA(dataframe['ap'], _total_length)

        # n1
        d = ta.EMA(abs(dataframe['ap'] - dataframe['esa']), _total_length * 2)
        dataframe['ci'] = (dataframe['ap'] - dataframe['esa']) / (0.015 * d)

        # n2
        dataframe['tci'] = ta.EMA(dataframe['ci'], _total_length)

        dataframe['wt1'] = dataframe['tci']
        dataframe['wt2'] = ta.EMA(dataframe['wt1'], _total_length) #4)

        dataframe['0'] = 0
        dataframe['-70'] = -70
        dataframe['-80'] = -80
        dataframe['70'] = 70
        dataframe['80'] = 80

        dataframe['ema_smoothed_goingup'] = dataframe['ema10smoothed'] > dataframe['ema10smoothed'].shift(1)
        dataframe['wt_goingup'] = dataframe['wt2'] > dataframe['wt2'].shift(1)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                # (qtpylib.crossed_above(dataframe['rsi'], 30)) &  # Signal: RSI crosses above 30
                # (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard: tema below BB middle
                # (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard: tema is raising
                # (dataframe['volume'] > 0)  # Make sure Volume is not 0

                # (dataframe['ema10'] > 9999)  # Make sure Volume is not 0

                (dataframe['ema_smoothed_goingup'].shift(1) == False) &
                (dataframe['ema_smoothed_goingup'] == False) &
                (dataframe['wt_goingup'].shift(1) == False) &
                (dataframe['wt_goingup'] == True) &
                (dataframe['wt2'] < -75)
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                (dataframe['ema_smoothed_goingup'].shift(1) == True) &
                (dataframe['ema_smoothed_goingup'] == True) &
                (dataframe['wt_goingup'].shift(1) == True) &
                (dataframe['wt_goingup'] == False) &
                (dataframe['wt2'] > 75)
            ),
            'sell'] = 1
        return dataframe
