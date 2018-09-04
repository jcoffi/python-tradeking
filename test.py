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
from simplejson import loads

import tradeking

conf = yaml.load(open('conf/credentials.yaml'))
TRADEKING_CONSUMER_KEY = conf['consumer']['ckey']
TRADEKING_CONSUMER_SECRET = conf['consumer']['csecret']
TRADEKING_ACCESS_TOKEN = conf['resource']['rkey']
TRADEKING_ACCESS_TOKEN_SECRET = conf['resource']['rsecret']
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

    url_path = "https://api.tradeking.com/v1/accounts/60792930/orders"
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
    print(quotes)
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
        #print(Desc)
        #print(OrdID)
        #print(TxnTm)
        #print(Txt)
        # This isn't done. We still need to sort out which OrdID is which.
        # But this gets us a hell of a lot closer


# def fixml_buy_now(ticker, quantity, limit):
#     """Generates the FIXML for a buy order."""
#
#     fixml = Element("FIXML")
#     fixml.set("xmlns", FIXML_NAMESPACE)
#     order = SubElement(fixml, "Order")
#     order.set("TmInForce", "0")  # Day order
#     order.set("Typ", "2")  # Limit
#     order.set("Side", "1")  # Buy
#     order.set("Px", "7")  # Limit price
#     order.set("Acct", "60792930")
#     instrmt = SubElement(order, "Instrmt")
#     instrmt.set("SecTyp", "CS")  # Common stock
#     instrmt.set("Sym", ticker)
#     ord_qty = SubElement(order, "OrdQty")
#     ord_qty.set("Qty", str(quantity))
#
#     return tostring(fixml)

def fixml_sell_trailingstop(ticker, quantity, limit):
    """Generates the FIXML for a trailing stop options order."""

    fixml = Element("FIXML")
    fixml.set("xmlns", FIXML_NAMESPACE)
    order = SubElement(fixml, "Order")
    order.set("TmInForce", "0")  # Day order
    order.set("Typ", "P")  # Trailing Stop
    order.set("Side", "2")  # Sell
    order.set("PosEfct", "C") # Needed for options "O" is for Open and "C" is for closing
    order.set("Acct", "60792930")
    order.set("ExecInst", "a")  # Can contain multiple instructions, space delimited. If OrdType=P, exactly one of the following values (ExecInst = L, R, M, P, O, T, or W) must be specified.
    peginstr = SubElement(order, "PegInstr")
    peginstr.set("OfstTyp", "1") # 0 for hard number, 1 for percentage
    peginstr.set("PegPxTyp", "1") # 1 means last price
    peginstr.set("OfstVal", "20")
    instrmt = SubElement(order, "Instrmt")
    instrmt.set("CFI", "OC") # Options Contracts
    instrmt.set("SecTyp", "OPT")  # Option or Stock
    instrmt.set("StrkPx", "10")
    instrmt.set("MMY", "201809")
    instrmt.set("MatDt", "2018-09-21T00:00:00.000-05:00")
    instrmt.set("Sym", ticker)
    undly = SubElement(order, "Undly")
    undly.set("Sym", ticker)
    ord_qty = SubElement(order, "OrdQty")
    ord_qty.set("Qty", "1")

    return tostring(fixml)

def make_request(url, method="GET", body="", headers=None):
    """Makes a request to the TradeKing API."""


    print("TradeKing request: %s %s %s %s" %
                    (url, method, body, headers))

    content = tkapi.account_order_preview(TRADEKING_ACCOUNT_NUMBER,fixml)

    #response,

    response = content

    print("TradeKing response: %s %s" % (response, content))

    try:
        return loads(content)
    except ValueError:
        print("Failed to decode JSON response: %s" % content)
        return None

tkapi = tradeking.TradeKingAPI(consumer_key=TRADEKING_CONSUMER_KEY,
                            consumer_secret=TRADEKING_CONSUMER_SECRET,
                            oauth_token=TRADEKING_ACCESS_TOKEN,
                            oauth_secret=TRADEKING_ACCESS_TOKEN_SECRET)

#testoptions = tkapi.market_options_expirations("VSTM")
#print(testoptions)
#fixml = fixml_sell_trailingstop(ticker2, qty, lmt)
#make_request(fixml)
#print(fixml)
get_account_orders(60792930)
#op_flag(str(ticker))
#market_cap(str(ticker))
