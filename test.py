import os
import requests
import yaml
import json
import re
import dpath.util
import lxml
from lxml import etree
from lxml import objectify
import xml.etree.ElementTree as et
from lxml.etree import Element
from lxml.etree import SubElement
from lxml.etree import tostring
#from io import StringIO


from requests_oauthlib import OAuth1

import tradeking

conf = yaml.load(open('conf/credentials.yaml'))
CONSUMER_KEY = conf['consumer']['ckey']
CONSUMER_SECRET = conf['consumer']['csecret']
OAUTH_TOKEN = conf['resource']['rkey']
OAUTH_SECRET = conf['resource']['rsecret']
TRADEKING_ACCOUNT_NUMBER = conf['accounts']['account']
# The XML namespace for FIXML requests.
FIXML_NAMESPACE = "http://www.fixprotocol.org/FIXML-5-0-SP2"

# The HTTP headers for FIXML requests.
FIXML_HEADERS = {"Content-Type": "text/xml"}

ticker2 = "VSTM"
qty = "500"
lmt = "-5"

def get_order_url():
    """Gets the TradeKing URL for placing orders."""

    url_path = "accounts/TRADEKING_ACCOUNT_NUMBER/orders"
    return url_path

def op_flag(ticker):
    quotes = tkapi.market_ext_quotes(ticker)
    isopt = dpath.util.get(quotes, "/quotes/quote/op_flag")
    return isopt

def market_cap(ticker):
    quotes = tkapi.market_ext_quotes(ticker)
    sho = dpath.util.get(quotes, "/quotes/quote/sho")
    last = dpath.util.get(quotes, "/quotes/quote/last")
    mktcap = (int(float(sho)) * int(float(last)))
    return mktcap

def get_account_orders(TRADEKING_ACCOUNT_NUMBER):
    quotes = tkapi.account_orders(TRADEKING_ACCOUNT_NUMBER)
    #print(quotes)
    #return loads(str(quotes))
    p = re.compile('<FIXML[\s\S]*?<\/FIXML>')
    orders = p.findall(str(quotes))
    print(orders)
    for order in orders:
        fmt_order = objectify.fromstring(order)
        objectify.deannotate(fmt_order, xsi_nil=True)
        Desc = fmt_order.ExecRpt.Instrmt.get('Desc')
        TxnTm = fmt_order.ExecRpt.get('TxnTm')
        Txt = fmt_order.ExecRpt.get('Txt')
        print(Desc)
        #print(OrdID)
        print(TxnTm)
        print(Txt)
        # This isn't done. We still need to sort out which OrdID is which.
        # But this gets us a hell of a lot closer

def fixml_sell_trailingstop(ticker, quantity, limit):
    """Generates the FIXML for a trailing stop order."""

    fixml = Element("FIXML")
    fixml.set("xmlns", FIXML_NAMESPACE)
    order = SubElement(fixml, "Order")
    order.set("TmInForce", "0")  # Day order
    order.set("Typ", "P")  # Trailing Stop
    order.set("Side", "2")  # Sell
    order.set("Acct", str(TRADEKING_ACCOUNT_NUMBER))
    order.set("ExecInst", "a")
    order = SubElement(fixml, "Order")
    peginstr = SubElement(order, "PegInstr")
    peginstr.set("OfstTyp", "1") # 0 for hard number, 1 for percentage
    peginstr.set("PegPxTyp", "1") # 1 means last price
    peginstr.set("OfstVal", str(limit))
    instrmt = SubElement(order, "Instrmt")
    instrmt.set("SecTyp", "OPT")  # Option or Stock
    instrmt.set("Sym", ticker)
    ord_qty = SubElement(order, "OrdQty")
    ord_qty.set("Qty", str(quantity))

    return tostring(fixml)

def make_order_request(fixml):
    """Executes an order defined by FIXML and verifies the response."""

    response = tkapi.account_order(account_id=TRADEKING_ACCOUNT_NUMBER,order=fixml)

    if not response:
        print("No order response for: %s" % fixml)
        return False

    try:
        order_response = response["response"]
        error = order_response["error"]
    except KeyError:
        print("Malformed order response: %s" % response)
        return False

    # The error field indicates whether the order succeeded.
    error = order_response["error"]
    if error != "Success":
        print("Error in order response: %s %s" %
                        (error, order_response))
        return False

    return True


tkapi = tradeking.TradeKingAPI(consumer_key=CONSUMER_KEY,
                            consumer_secret=CONSUMER_SECRET,
                            oauth_token=OAUTH_TOKEN,
                            oauth_secret=OAUTH_SECRET)


fixml = fixml_sell_trailingstop(ticker2, qty, lmt)
make_order_request(fixml)
#get_account_orders(TRADEKING_ACCOUNT_NUMBER)
#op_flag(str(ticker))
#market_cap(str(ticker))
