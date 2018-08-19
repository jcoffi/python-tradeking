import os
import requests
import yaml
import json
import dpath.util

from requests_oauthlib import OAuth1

import tradeking

conf = yaml.load(open('conf/credentials.yaml'))
CONSUMER_KEY = conf['consumer']['ckey']
CONSUMER_SECRET = conf['consumer']['csecret']
OAUTH_TOKEN = conf['resource']['rkey']
OAUTH_SECRET = conf['resource']['rsecret']

def op_flag(stock):
    quotes = tkapi.market_ext_quotes(stock)
    isopt = dpath.util.get(quotes, "/quotes/quote/op_flag")
    return isopt

def market_cap(stock):
    quotes = tkapi.market_ext_quotes(stock)
    sho = dpath.util.get(quotes, "/quotes/quote/sho")
    last = dpath.util.get(quotes, "/quotes/quote/last")
    mktcap = (int(float(sho)) * int(float(last)))
    return mktcap

tkapi = tradeking.TradeKingAPI(consumer_key=CONSUMER_KEY,
                            consumer_secret=CONSUMER_SECRET,
                            oauth_token=OAUTH_TOKEN,
                            oauth_secret=OAUTH_SECRET)


op_flag("VSTM")
market_cap("VSTM")
