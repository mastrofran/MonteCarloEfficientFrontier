#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 21:11:57 2018

@author: mauricedentallab
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quandl
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
import time


def last_date(tickers = []):
    quandl.ApiConfig.api_key= "3PMrCbmFBBWqH9YQ1tBW"
    quandl_stocks = []
    for ticker in tickers:
        quandl_stocks.append("WIKI/" + ticker + ".11")
    stocks_to_analyze = quandl.get(quandl_stocks, start_date=startDate, end_date=None, transform = "adj_close", paginate = True)
    stocks_to_analyze.columns = tickers
    datedf = stocks_to_analyze.reset_index()
    print(datedf['Date'].iloc[-1])
    return datedf['Date'].iloc[-1]

def return_funct(row):
    return ((row - row[0])/row[0])*100

def annualized_returns(row):
    return (((row[-1]-row[0])/row[0])*100)/years

def get_stocks(tickers=[], answer = ' ' ):
    global stocks_date1
    quandl.ApiConfig.api_key= "3PMrCbmFBBWqH9YQ1tBW"
    quandl_stocks = []
    for ticker in tickers:
        quandl_stocks.append("WIKI/" + ticker + ".11")
    stocks_to_analyze = quandl.get(quandl_stocks, start_date=startDate, end_date=endDate, transform = "adj_close")
    stocks_to_analyze.columns = tickers
    print(stocks_to_analyze)
    if (answer is 'yes'):
        pct_return = stocks_to_analyze.apply(return_funct)
        return pct_return
    else:
        return stocks_to_analyze

    
def monte_carlo(tickers = []):
    quandl.ApiConfig.api_key= "3PMrCbmFBBWqH9YQ1tBW"
    quandl_stocks = []
    for ticker in tickers:
        quandl_stocks.append("WIKI/" + ticker + ".11")
    stocks_to_analyze = quandl.get(quandl_stocks, start_date=startDate, end_date=endDate, transform = "adj_close", paginate = True)
    stocks_to_analyze.columns = tickers
    print(stocks_to_analyze)
    port_returns = []
    port_volatility = []
    sharpe_ratio = []
    stock_weights = []
    
    # set the number of combinations for imaginary portfolios
    num_assets = len(stock_list)
    num_portfolios = 50000
    returns_daily = stocks_to_analyze.pct_change()
    returns_annual = stocks_to_analyze.apply(annualized_returns)
    cov_daily = returns_daily.cov()
    cov_annual = cov_daily * 250
    
    #set random seed for reproduction's sake
    np.random.seed(101)
    
    # populate the empty lists with each portfolios returns,risk and weights
    for single_portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        returns = np.dot(weights, returns_annual)
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
        sharpe = returns / volatility
        sharpe_ratio.append(sharpe)
        port_returns.append(returns)
        port_volatility.append(volatility)
        stock_weights.append(weights)
    
    # a dictionary for Returns and Risk values of each portfolio
    portfolio = {'Returns': port_returns,
                 'Volatility': port_volatility,
                 'Sharpe Ratio': sharpe_ratio}
    
    # extend original dictionary to accomodate each ticker and weight in the portfolio
    for counter,symbol in enumerate(stock_list):
        portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]
    
    # make a nice dataframe of the extended dictionary
    df = pd.DataFrame(portfolio)
    
    # get better labels for desired arrangement of columns
    column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in stock_list]
    
    # reorder dataframe columns
    df = df[column_order]
    
    min_volatility = df['Volatility'].min()
    max_sharpe = df['Sharpe Ratio'].max()
    
    # use the min, max values to locate and create the two special portfolios
    sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
    min_variance_port = df.loc[df['Volatility'] == min_volatility]
    
    # plot frontier, max sharpe & min Volatility values with a scatterplot
    plt.style.use('seaborn-dark')
    df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                    cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
    plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='o', s=200)
    plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='o', s=200 )
    plt.xlabel('Volatility')
    plt.ylabel('Expected Returns')
    plt.title('Efficient Frontier')
    plt.show()
    print(min_variance_port.T)
    print(sharpe_portfolio.T)
    
    
stock_list = ['QTRX', 'NVDA']
ts = TimeSeries(key='GDOW0X6D1UESDBGI', output_format='pandas')


startDate = '2016-01-01'
d1 = datetime.strptime(startDate, "%Y-%m-%d")
date_difference = abs((last_date(stock_list)-d1).days)
endDate = datetime.strftime(last_date(stock_list), "%Y-%m-%d")
years = date_difference/365
ax = get_stocks(stock_list, answer = 'yes').plot()
ax.set_ylabel('% Return')
monte_carlo(stock_list)
