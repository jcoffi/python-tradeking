import yaml
conf = yaml.load(open('conf/credentials.yaml'))
ALLY_CONSUMER_KEY = conf['consumer']['ckey']
ALLY_CONSUMER_SECRET = conf['consumer']['csecret']
ALLY_ACCESS_TOKEN = conf['resource']['rkey']
ALLY_ACCESS_TOKEN_SECRET = conf['resource']['rsecret']
ALLY_ACCOUNT_NUMBER = conf['accounts']['account']
import dpath.util
from rauth import OAuth1Session

ally = OAuth1Session(
        consumer_key=ALLY_CONSUMER_KEY,
        consumer_secret=ALLY_CONSUMER_SECRET,
        access_token=ALLY_ACCESS_TOKEN,
        access_token_secret=ALLY_ACCESS_TOKEN_SECRET
        )

params = {'symbols': ('VSTM'), 'fids': 'last,pvol,sho',
          #'consumer_key': ALLY_CONSUMER_KEY,
          #'consumer_secret': ALLY_CONSUMER_SECRET,
          #'access_token': ALLY_ACCESS_TOKEN,
          #'access_token_secret': ALLY_ACCESS_TOKEN_SECRET,
#          'request_token_url': ALLY_REQUEST_TOKEN_URL,
#          'access_token_url': ALLY_ACCESS_TOKEN_RETRIEVAL_URL,
#          'authorize_url': ALLY_USER_AUTHORIZATION_URL,
          'base_url': 'https://api.tradeking.com/v1/'
         }
r = ally.get('https://api.tradeking.com/v1/market/ext/quotes.json',
             params=params)
print(r.json())

def market_cap(ticker):
    quotes = r = ally.get('https://api.tradeking.com/v1/market/ext/quotes.json'),
    sho = dpath.util.get(quotes, "/quotes/quote/sho"),
    last = dpath.util.get(quotes, "/quotes/quote/last"),
    mktcap = (int(float(sho)) * int(float(last)))
    return mktcap
