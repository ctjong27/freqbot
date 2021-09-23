# Prepare source
source .env/bin/activate

# Commands
## Data is stored in /user_data/
**Adding Files**
- Add Freqtrade User
    - `freqtrade create-userdir --userdir user_data/`
- Verify Git Ignores Case Difference
    - `git config core.ignorecase true`
- Add Freqtrade Config
    - `freqtrade new-config --config CONFIG_.json`
    - https://www.freqtrade.io/en/latest/configuration/
- Add Freqtrade Strategy
    - `freqtrade new-strategy --strategy STRATEGY_`
    - https://www.freqtrade.io/en/latest/strategy-customization/
- Add Hyperopt
    - `freqtrade new-hyperopt --hyperopt HYPEROPT_`
    - https://www.freqtrade.io/en/latest/hyperopt/

**Running**
- Run Freqtrade
    - `freqtrade trade -c EMA_CROSSOVER_CONFIG.json -s EMA_CROSSOVER_STRATEGY`

- Commands
    - choose from 'trade', 'create-userdir', 'new-config', 'new-hyperopt', 'new-strategy', 'download-data', 'convert-data', 'convert-trade-data', 'backtesting', 'edge', 'hyperopt', 'hyperopt-list', 'hyperopt-show', 'list-exchanges', 'list-hyperopts', 'list-markets', 'list-pairs', 'list-strategies', 'list-timeframes', 'show-trades', 'test-pairlist', 'plot-dataframe', 'plot-profit'

# Back Testing
- Data Download
    - Data pairs retrieved from config.json or pairs.json
        - /user_data/data/binance/pairs.json 
    - `freqtrade download-data --exchange binance`
    - `freqtrade download-data --exchange binance --timeframes 1m 5m 15m 30m 1h 6h 1d`
    - `freqtrade download-data --exchange binance --pairs XRP/ETH ETH/BTC --days 20 --dl-trades`
    - `freqtrade download-data --exchange binance --timeframes 5m 15m 30m 1h 6h 1d --days 300`
    - `freqtrade download-data --exchange binance --timeframes 5m 15m 30m 1h 6h 12h 1d --days 300`
    - `freqtrade download-data --exchange binance --timeframes 30m 1h 12h 1d --days 1200`
    - `freqtrade download-data --exchange binance --pairs ETH/BTC --timeframes 1h 2h 4h 12h 1d --days 1200`
    - https://www.freqtrade.io/en/latest/data-download/

- Run Backtest
    - `freqtrade backtesting -c CONFIG_.json -s STRATEGY_`
    - `freqtrade backtesting -c CONFIG_.json -s STRATEGY_ --timeframe 15m`
    - `freqtrade backtesting -c CONFIG_.json -s STRATEGY_ --timeframe 15m --timerange=20180501-20200715`
    - https://www.freqtrade.io/en/latest/backtesting/

- Plot
    - `freqtrade plot-dataframe -c CONFIG_.json -s STRATEGY_`
    - `freqtrade plot-dataframe -c CONFIG_.json -s STRATEGY_ --timeframe 15m`
    - `freqtrade plot-dataframe -c CONFIG_.json -s STRATEGY_ --timeframe 15m --timerange=20180501-20200715`
    - https://www.freqtrade.io/en/latest/backtesting/

# Set strategy


# Set hyperopt for each strategy


# set config for each strategy