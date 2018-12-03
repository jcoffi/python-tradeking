import yaml
conf = yaml.load(open('conf/credentials.yaml'))
ALLY_CONSUMER_KEY = conf['consumer']['ckey']
ALLY_CONSUMER_SECRET = conf['consumer']['csecret']
ALLY_ACCESS_TOKEN = conf['resource']['rkey']
ALLY_ACCESS_TOKEN_SECRET = conf['resource']['rsecret']
ALLY_ACCOUNT_NUMBER = conf['accounts']['account']
import dpath.util
import sys
from rauth import OAuth1Session

ally = OAuth1Session(
        consumer_key=ALLY_CONSUMER_KEY,
        consumer_secret=ALLY_CONSUMER_SECRET,
        access_token=ALLY_ACCESS_TOKEN,
        access_token_secret=ALLY_ACCESS_TOKEN_SECRET
        )

ticker = str(sys.argv[1])

params = {'symbols': (ticker), 'fids': 'last,pvol,sho',
          'base_url': 'https://api.tradeking.com/v1/'
         }
r = ally.get('https://api.tradeking.com/v1/market/ext/quotes.json',
             params=params)
print(r.json())

#def op_flag(ticker):
#    quotes = r = ally.get('https://api.tradeking.com/v1/market/ext/quotes.json'),
#    isopt = dpath.util.get(quotes, "/quotes/quote/op_flag"),
#    return isopt

def market_cap(ticker):
    quotes = r = ally.get('https://api.tradeking.com/v1/market/ext/quotes.json'),
    sho = dpath.util.get(quotes, "/quotes/quote/sho"),
    last = dpath.util.get(quotes, "/quotes/quote/last"),
    mktcap = (int(float(sho)) * int(float(last))),
    return mktcap
