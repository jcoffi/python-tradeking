"""Using rauth library maintained by Max Countryman"""
from rauth import OAuth1Session
"""set application keys issued by TradeKing website when a new developer
application is created; personal keys are not hard coded here for
security reasons"""
import yaml
conf = yaml.load(open('conf/credentials.yaml'))
cKey = conf['consumer']['ckey']
cSecret = conf['consumer']['csecret']
oKey = conf['resource']['rkey']
oSecret = conf['resource']['rsecret']
account = conf['accounts']['account']

"""Use the keys to instantiate a session"""
tradeking = OAuth1Session(
				name='tradeking',
				consumer_key = cKey,
				consumer_secret = cSecret,
				access_token = oKey,
				access_token_secret = oSecret,
				base_url='https://api.tradeking.com/v1')



def _get(self, request, params=None):
	"""HTTP GET request"""
	url = '%s/%s.json' % (ENDPOINT, request) #This will need to be rewritten to use rauth. Right now this will generate a TypeError: 'OAuth1Service' object is not callable error.
	return tradeking.get(url, params=params).json().get('response')

def _post(self, request, data):
	"""HTTP POST request"""
	url = '%s/%s.json' % (ENDPOINT, request) #This will need to be rewritten to use rauth. Right now this will generate a TypeError: 'OAuth1Service' object is not callable error.
	return tradeking.post(url, data=data).json().get('response')

def accounts(self):
	"""This call will return detailed balance and holding information for
	each account associated with a user."""
	return self._get('accounts')

def accounts_balances(self):
	"""This call will return summary balance information for each account
	associated with a user as well as the total value for all accounts
	associated with a user."""
	return self._get('accounts/balances')

def account(self, account_id):
	"""This call will return detailed balance and holding information for
	the account number specified in the URI."""
	return self._get('accounts/%s' % account_id)

def account_balances(self, account_id):
	"""This call will return detailed balance information for the account
	number specified in the URI."""
	return self._get('accounts/%s/balances' % account_id)

def account_history(self, account_id):
	"""This call will return account activity for the account number
	specified in the URI. This call supports optional date range or
	transaction type filters."""
	return self._get('accounts/%s/history' % account_id)

def account_holdings(self, account_id):
	"""This call will return detail information about the holdings for an
	account specified in the URI."""
	return self._get('accounts/%s/holdings' % account_id)

def account_orders(self, account_id):
	"""This call will return the most recent orders for the account
	specified in the URI."""
	return self._get('accounts/%s/orders' % account_id)

def account_order(self, account_id, order):
	"""This call will allow you to place an order. This requires the order
	data is submitted in FIXML format submitted as XML within the body."""
	url = 'accounts/%s/orders' % account_id
	return self._post(url, order)

def account_order_preview(self, account_id, order):
	"""This call will allow you to preview an order prior to actually
	placing it. This does not place the order."""
	url = 'accounts/%s/orders/preview' % account_id
	return self._post(url, order)

def market_clock(self):
	"""This call will return the current state of the market, the time of
	the next state change (if the market is open), and the current server
	timestamp."""
	return self._get('market/clock')

def market_ext_quotes(self, symbols, fids=None):
	"""This call will return quotes for a symbol or list of symbols passed
	as a query parameter."""
	params = dict(symbols=symbols, fids=fids)
	return self._get('market/ext/quotes', params=params)

def market_news_search(self, keywords=None, symbols=None,
					   maxhits='10', startdate=None, enddate=None):
	"""This call will return a listing of news headlines based on the
	current keyword and/or symbol search."""
	params = dict(keywords=keywords,
				  symbols=symbols,
				  maxhits=maxhits,
				  startdate=startdate,
				  enddate=enddate)
	return self._get('market/news/search', params=params)

def market_news(self, news_id):
	"""This call will return an article identified by the URI id."""
	return self._get('market/news/%s' % news_id)

def market_options_search(self, symbol, query=None, fids=None):
	"""This call will return the full list of available option strikes for
	a given symbol."""
	params = dict(symbol=symbol, query=query, fids=fids)
	return self._get('market/options/search', params=params)

def market_options_strikes(self, symbol):
	"""This call will return the full list of available option strikes for
	a given symbol."""
	params = dict(symbol=symbol)
	return self._get('market/options/strikes', params=params)

def market_options_expirations(self, symbol):
	"""This call will return the full list of available option expiration
	dates for a given symbol."""
	params = dict(symbol=symbol)
	return self._get('market/options/expirations', params=params)

def market_timesales(self, symbols, interval='5min', rpp='10', index=None,
					 startdate=None, enddate=None, starttime=None):
	"""This call will return time and sales quote data based on a symbol
	passed as a query parameter."""
	params = dict(symbols=symbols,
				  interval=interval,
				  rpp=rpp,
				  index=index,
				  startdate=startdate,
				  enddate=enddate,
				  starttime=starttime)
	return self._get('market/timesales', params=params)

def market_toplists(self, list_type):
	"""This call will return a ranked list based on the list type
	specified."""
	return self._get('market/toplists/%s' % list_type)

def member_profile(self):
	"""This call will return general information associated with the user.
	More importantly it will also return all of the account numbers and
	account information for the user."""
	return self._get('member/profile')

def utility_status(self):
	"""This call will return the current server timestamp if the API and
	its backend systems are accessible. Otherwise it will return an
	error."""
	return self._get('utility/status')

def utility_version(self):
	"""This call will return the version of the API of the endpoint
	called."""
	return self._get('utility/version')




"""Set the get request parameters"""
params = {'symbols': 'aapl,nflx,fb', 'fids': 'last,pvol,pcls'}

"""Fetch data market quotes data"""
r = tradeking.get('https://api.tradeking.com/v1/market/ext/quotes.json',
						params = params)

	"""Parse JSON object"""
	json_obj = r.json()
	#print("\nStock: Last Price, Exchange, Previous Day Volume, Previous Day Close\n")
	print(json_obj)

#for dict_item in list((json_obj['response']['quotes']['quote'])):
	#symb = dict_item['symbols']
#	last_price = dict_item['last']
	#exchange = dict_item['exch']
#	prev_day_vol = dict_item['pvol']
#	prev_day_close = dict_item['pcls']
#	print (u'{0}: {1} {2} {3} {4}'.format(symb, last_price, exchange,
#										  prev_day_vol, prev_day_close))
