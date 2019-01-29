# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 19:15:01 2019

@author: Francesco
"""

import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import json
import time
from scipy import stats
import sys
import os

initial_time = time.time()

def MonteCarlo(tickers = []):
    full_data = pd.DataFrame()
    for ticker in tickers:
        get_tickers = pd.read_csv('%s_Close.csv'%ticker)
        get_tickers.columns = ['Date', ticker]
        pd.to_datetime(get_tickers['Date'])
        get_tickers = get_tickers.set_index('Date')
        get_tickers = get_tickers.sort_values(by='Date')
        full_data = pd.concat([full_data, get_tickers], axis=1, sort = True)
    full_data = full_data.dropna()
    full_data = full_data[tickers]
    d1 = full_data.index[0]
    d2 = full_data.index[-1]
    date_difference = abs((pd.to_datetime(d2)-pd.to_datetime(d1)).days)
    years = date_difference/365
    Total_fractional_change = (full_data.iloc[-1, :] / full_data.iloc[0, :])
    Total_fractional_change = pd.DataFrame.from_dict(Total_fractional_change)
    Total_fractional_change = Total_fractional_change.rename(columns = {0: 'Total % Change'})
    annual_percent_change = ((Total_fractional_change**(1/years))-1)*100
    
    port_returns = []
    port_volatility = []
    sharpe_ratio = []
    stock_weights = []

    
    # set the number of combinations for imaginary portfolios
    num_assets = len(tickers)
    num_portfolios = 50000
    returns_daily = full_data[tickers].pct_change()*100
    returns_daily = returns_daily.dropna()
    std_daily = returns_daily.std()
    std_annual = std_daily * (252**0.5)
    #set random seed for reproduction's sake
    np.random.seed(101)
    
    # populate the empty lists with each portfolios returns,risk and weights
    for single_portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        returns = np.dot(weights, annual_percent_change)
        returns = returns.item(0)
        volatility = np.dot(weights, std_annual.values)
        sharpe = (returns - risk_free_rate) / (volatility)
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
        portfolio[symbol] = [Weight[counter] for Weight in stock_weights]
    
    # make a nice dataframe of the extended dictionary
    df = pd.DataFrame(portfolio)
    
    # get better labels for desired arrangement of columns
    column_order = ['Expected Annual Returns', 'Volatility', 'Sharpe Ratio'] + [stock for stock in tickers]
    
    # reorder dataframe columns
    df = df[column_order]
    max_sharpe = df['Sharpe Ratio'].max()
    
    # use the min, max values to locate and create the two special portfolios
    sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
    montecarlo = sharpe_portfolio.T
    montecarlo_tickers = pd.DataFrame.to_dict(montecarlo[3:])
    montecarlo_dict = {'startDate': d1,
                 'endDate': d2,
                 'returns':montecarlo.iloc[0][montecarlo.columns[0]],
                 'volatility': montecarlo.iloc[1][montecarlo.columns[0]],
                 'sharpeRatio': montecarlo.iloc[2][montecarlo.columns[0]],
                 'weights' : list(montecarlo_tickers.values())}
    montecarlo_dump = json.dumps(montecarlo_dict, indent = 4)
    return montecarlo_dump

risk_free_rate = 2.36
tickers = sys.argv[1]
path = 'C:\\Users\Francesco\Desktop\Python_Scripts\Portfolio-Project\Stock_Data'
os.chdir(path)
montecarlo_JSON = MonteCarlo(tickers)
print(montecarlo_JSON)
sys.stdout.flush()

