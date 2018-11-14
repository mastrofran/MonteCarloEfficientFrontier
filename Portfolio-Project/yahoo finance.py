# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 15:25:23 2018

@author: Francesco
"""

from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
from datetime import date
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Definition Clean Up Data Incoming from YF
def cleanUp(tickers=[]):
    counter = 1
    for ticker in tickers:
        data = pdr.get_data_yahoo(ticker, start=startDate, end=endDate)
        adjClose = data['Adj Close']
        adjClose = pd.DataFrame({'Date': adjClose.index, 'Adj Close':adjClose.values})
        adjClose.rename(index=str, columns={"Adj Close": ticker}, inplace = True)
#        for index, row in adjClose.iterrows():
#            adjClose['initial'] = adjClose.iloc[0][ticker]
#        adjClose['pct_change'] = ((adjClose[ticker] - adjClose['initial'])/adjClose['initial'])*100
#        adjClose.rename(index=str, columns={"Adj Close": ticker, "initial": "%s Initial" % (ticker)}, inplace = True)
        if counter == 2:
            combined = pd.merge(data_old, adjClose, on='Date')
        data_old = adjClose
        if counter >2:
            combined = pd.merge(combined, adjClose, on = 'Date')
        counter+=1
    counter = 1
    tickers_pct_change =[]
    for item in tickers:
        combined['initial'] = combined.iloc[0][item]
        combined['pct_change'] = ((combined[item] - combined['initial'])/combined['initial'])*100
        combined.rename(index=str, columns={"initial": "%s Initial" % (item), "pct_change": "%s Pct Change" % (item)}, inplace = True)
        tickers_pct_change.append("%s Pct Change" % (item))
        print(item, 'Total % Change: ', combined.iloc[-1]["%s Pct Change" % (item)])
        print(combined.iloc[0][item], combined.iloc[-1][item])
    combined.plot(x='Date',y=tickers_pct_change, grid=True)
    return combined

def monte_carlo(tickers = []):
    port_returns = []
    port_volatility = []
    sharpe_ratio = []
    stock_weights = []
    
    # set the number of combinations for imaginary portfolios
    num_assets = len(tickers)
    num_portfolios = 50000
    returns_daily = full_data[tickers].pct_change()
    returns_annual = ((full_data.iloc[-1][tickers] - full_data.iloc[0][tickers])*100/full_data.iloc[0][tickers])/years
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
    portfolio = {'Expected Annual Returns': port_returns,
                 'Volatility': port_volatility,
                 'Sharpe Ratio': sharpe_ratio}
    
    # extend original dictionary to accomodate each ticker and weight in the portfolio
    for counter,symbol in enumerate(tickers):
        portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]
    
    # make a nice dataframe of the extended dictionary
    df = pd.DataFrame(portfolio)
    
    # get better labels for desired arrangement of columns
    column_order = ['Expected Annual Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in tickers]
    
    # reorder dataframe columns
    df = df[column_order]
        
    min_volatility = df['Volatility'].min()
    max_sharpe = df['Sharpe Ratio'].max()
    
    # use the min, max values to locate and create the two special portfolios
    sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
    min_variance_port = df.loc[df['Volatility'] == min_volatility]
    
    # plot frontier, max sharpe & min Volatility values with a scatterplot
    plt.style.use('seaborn-dark')
    df.plot.scatter(x='Volatility', y='Expected Annual Returns', c='Sharpe Ratio',
                    cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
    plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Expected Annual Returns'], c='red', marker='o', s=200, label = 'Max Sharpe')
    plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Expected Annual Returns'], c='blue', marker='o', s=200, label = 'Min Vol')
    plt.xlabel('Volatility')
    plt.ylabel('Expected Annual Returns')
    plt.title('Efficient Frontier')
    plt.legend()
    plt.show()
    print('Since %s, an optimized portfolio with regards to minimum volitility would consist of the following weights: ' %d1, min_variance_port.T)
    print('Since %s, an optimized portfolio with regards to highest sharpe ratio would consist of the following weights: ' %d1, sharpe_portfolio.T)

tickers = ['GOOG', 'TSLA', 'FB', 'MMM', 'SPY', 'BRK-B', 'BRK-A', 'V', 'C', 'GE', 'BLK', 'BNS']
startDate = "2012-05-25"
endDate = str(date.today())
# Plot Pct Returns Over time
full_data = cleanUp(tickers)
first_date_in_set = full_data.iloc[0]['Date']
last_date_in_set = full_data.iloc[-1]['Date']
d1 = pd.to_datetime(first_date_in_set)
d2 = pd.to_datetime(last_date_in_set)
date_difference = abs((d2-d1).days)
years = date_difference/365
monte_carlo(tickers)



