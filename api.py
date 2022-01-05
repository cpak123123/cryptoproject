import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
class Crypto:
    global base
    global test
    base = "https://api.binance.com/"
    test = "api/v3/time"
    def __init__(self):
        # print(requests.request("GET", base+test))
        pass
    def current_sym(self, ticks):
        exchange = "api/v3/exchangeInfo?symbol="
        resp = requests.request("GET", base + exchange + ticks)
        return resp.json()

        #update: please use klines api to get hist data :)
    def hist(self, tick = "BTCUSDT", backlog = 5):
        old = "api/v3/trades"
        symbol = "?symbol=" + tick
        limit = "limit=" + str(backlog)
        st = "start"
        resp = requests.request("GET", base + old + symbol + "&" + limit)
        return resp.json()

    def hist_new(self, tick = "BTCUSDT", interval = '1d',  st = np.datetime64("now") - np.timedelta64(30, 'D'), et = np.datetime64("now")):
        order = {}
        old = "api/v3/klines"
        order["symbol"] = tick
        order["interval"] = interval
        order["startTime"] = str(self.to_ms(st))
        order["endTime"] = str(self.to_ms(et))
        resp = requests.request("GET", base + old, params= order)
        his = pd.DataFrame(resp.json(), columns=["opentime", "open", "high", "low", "close", "volume", "closetime", "qav", "ntrades", "tbav", "tqav", "ig"])
        his = his.astype(float)
        his["timestamps"] = pd.date_range(st, et, len(his))
        return his
    
    def to_ts(self, ms):
        target_dt = np.datetime64("1970-01-01") + np.timedelta64(ms, 'ms')
        return target_dt

    def to_ms(self, ts):
        ms = ts.astype(np.int64)*1000
        return ms
