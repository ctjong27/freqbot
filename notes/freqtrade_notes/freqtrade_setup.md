https://www.freqtrade.io/en/latest/installation/

In VSCode, view .md files with ctrl+shift+v

# Installing freqtrade to developer machine

- git clone https://github.com/freqtrade/freqtrade.git
    - cd freqtrade
    - git checkout master
    - ./setup.sh --install

- source .env/bin/activate
    - python -m pip install -e .
    - pip install -r requirements-hyperopt.txt



# Set config.json
- Api key from Binance
- Telegram set as true and set fields
    - BotFather for new bot & bot token
    - @get_id_bot to get chat id

# continue to freqtrade_run.md
