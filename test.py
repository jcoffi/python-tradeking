import os
import requests
import yaml
import json
import re
import dpath.util
import lxml
from lxml import etree
#from lxml import objectify
import xml.etree.ElementTree as et
#from io import StringIO


from requests_oauthlib import OAuth1

import tradeking

conf = yaml.load(open('conf/credentials.yaml'))
CONSUMER_KEY = conf['consumer']['ckey']
CONSUMER_SECRET = conf['consumer']['csecret']
OAUTH_TOKEN = conf['resource']['rkey']
OAUTH_SECRET = conf['resource']['rsecret']
account = conf['accounts']['account']

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

def account_orders(account):
    quotes = tkapi.account_orders(account)
    #return loads(str(quotes))
    #sho = dpath.util.values(quotes, '/orderstatus/order')
    #sho = re.sub('\[\[{.*fixmlmessage.*?>', '', str(sho))
#    sho = re.sub('^.*?>', '', str(sho))
    #sho = re.sub('\'}\]\]', '', str(sho))
    #e = et.fromstring(sho).getroot()
    #for atype in e.findall('ExecRpt'):
    #    print(atype.get('OrdID'))


    print(json.dumps(quotes, indent=4, ensure_ascii=False, cls=None))

tkapi = tradeking.TradeKingAPI(consumer_key=CONSUMER_KEY,
                            consumer_secret=CONSUMER_SECRET,
                            oauth_token=OAUTH_TOKEN,
                            oauth_secret=OAUTH_SECRET)

account_orders(account)
op_flag("VSTM")
market_cap("VSTM")
