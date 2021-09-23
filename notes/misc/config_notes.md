# Configuration Notes

- For buy, "use_order_book": true # getting bid
    - should be set for sandbox/live
- For buy, "use_order_book": false # getting ask (worst case scenario)
    - should be set for simulation and backtesting
- For sell, "use_order_book": false # getting ask (worst case scenario)
    - all the time, because you want to ensure fast sell