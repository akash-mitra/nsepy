# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 21:51:41 2015

@author: SW274998
"""
import pdb
from nsepy.commons import *
import ast
import json
from bs4 import BeautifulSoup
from nsepy.liveurls import quote_eq_url, quote_derivative_url, option_chain_url, holiday_list_url

OPTIONS_CHAIN_SCHEMA = [str, int, int, int, float, float, float, int, float, float, int,
                        float,
                        int, float, float, int, float, float, float, int, int, int, str]
OPTIONS_CHAIN_HEADERS = ["Call Chart", "Call OI", "Call Chng in OI", "Call Volume", "Call IV", "Call LTP", "Call Net Chng", "Call Bid Qty", "Call Bid Price", "Call Ask Price", "Call Ask Qty",
                         "Strike Price",
                         "Put Bid Qty", "Put Bid Price", "Put Ask Price", "Put Ask Qty", "Put Net Chng", "Put LTP", "Put IV", "Put Volume", "Put Chng in OI", "Put OI", "Put Chart"]
OPTIONS_CHAIN_INDEX = "Strike Price"

eq_quote_referer = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={}&illiquid=0&smeFlag=0&itpFlag=0"
derivative_quote_referer = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?underlying={}&instrument={}&expiry={}&type={}&strike={}"
option_chain_referer = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=-9999&symbol=NIFTY&symbol=BANKNIFTY&instrument=OPTIDX&date=-&segmentLink=17&segmentLink=17"


def get_quote(symbol, series='EQ', instrument=None, expiry=None, option_type=None, strike=None):
    """
    1. Underlying security (stock symbol or index name)
    2. instrument (FUTSTK, OPTSTK, FUTIDX, OPTIDX)
    3. expiry (ddMMMyyyy)
    4. type (CE/PE for options, - for futures
    5. strike (strike price upto two decimal places
    """
    if instrument:
        expiry_str = "%02d%s%d" % (
            expiry.day, months[expiry.month][0:3].upper(), expiry.year)
        quote_derivative_url.session.headers.update(
            {'Referer': eq_quote_referer.format(symbol)})
        strike_str = "{:.2f}".format(strike) if strike else ""
        res = quote_derivative_url(
            symbol, instrument, expiry_str, option_type, strike_str)
    else:
        quote_eq_url.session.headers.update(
            {'Referer': eq_quote_referer.format(symbol)})
        res = quote_eq_url(symbol, series)

    html_soup = BeautifulSoup(res.text, 'lxml')
    hresponseDiv = html_soup.find("div", {"id": "responseDiv"})
    d = json.loads(hresponseDiv.get_text())
    #d = json.loads(res.text)['data'][0]
    res = {}
    for k in d.keys():
        v = d[k]
        try:
            v_ = None
            if v.find('.') > 0:
                v_ = float(v.strip().replace(',', ''))
            else:
                v_ = int(v.strip().replace(',', ''))
        except:
            v_ = v
        res[k] = v_
    return res


def get_option_chain(symbol, instrument=None, expiry=None):

    if expiry:
        expiry_str = "%02d%s%d" % (
            expiry.day, months[expiry.month][0:3].upper(), expiry.year)
    else:
        expiry_str = "-"
    option_chain_url.session.headers.update({'Referer': option_chain_referer})
    r = option_chain_url(symbol, instrument, expiry_str)

    return r


def get_option_chain_table(symbol, instrument=None, expiry=None):
    optchainscrape = get_option_chain(symbol, instrument, expiry)
    html_soup = BeautifulSoup(optchainscrape.text, 'html.parser')
    sptable = html_soup.find("table", {"id": "octable"})
    tp = ParseTables(soup=sptable,
                     schema=OPTIONS_CHAIN_SCHEMA,
                     headers=OPTIONS_CHAIN_HEADERS, index=OPTIONS_CHAIN_INDEX)
    return tp.get_df()


def get_holidays_list(fromDate,
                      toDate):
    """This is the function to get exchange holiday list between 2 dates.
        Args:
            fromDate (datetime.date): start date
            toDate (datetime.date): end date
        Returns:
            pandas.DataFrame : A pandas dataframe object
        Raises:
            ValueError:
                        1. From Date param is greater than To Date param
    """
    if fromDate > toDate:
        raise ValueError('Please check start and end dates')

    holidayscrape = holiday_list_url(fromDate.strftime(
        "%d-%b-%Y"), toDate.strftime("%d-%b-%Y"))
    html_soup = BeautifulSoup(holidayscrape.text, 'lxml')
    sptable = html_soup.find("table")
    tp = ParseTables(soup=sptable,
                     schema=[str, StrDate.default_format(
                         format="%d-%b-%Y"), str, str],
                     headers=["Market Segment", "Date", "Day Of the Week", "Description"], index="Date")
    dfret = tp.get_df()
    dfret = dfret.drop(["Market Segment"], axis=1)
    return dfret
