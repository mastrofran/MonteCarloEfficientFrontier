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

initial_time = time.time()

def MonteCarlo(tickers = []):
    global sharpe_portfolio
    global min_variance_port
    global df
    global std_daily
    global std_annual
    global portfolio
    global weights
    port_returns = []
    port_volatility = []
    sharpe_ratio = []
    stock_weights = []

    
    # set the number of combinations for imaginary portfolios
    num_assets = len(tickers)
    num_portfolios = 50000
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
    
    return sharpe_portfolio.T

def MonteCarloToJSON(montecarlo, tickers =[]):
    montecarlo_tickers = pd.DataFrame.to_dict(montecarlo[3:])
    montecarlo_dict = {'returns':montecarlo.iloc[0][montecarlo.columns[0]],
                 'volatility': montecarlo.iloc[1][montecarlo.columns[0]],
                 'sharpeRatio': montecarlo.iloc[2][montecarlo.columns[0]],
                 'weights' : list(montecarlo_tickers.values())}
    montecarlo_dump = json.dumps(montecarlo_dict, indent = 4)
    return montecarlo_dump

def PortfolioChange(returns_daily, montecarlo):
    global weighted_daily_return
    montecarlo_dict = pd.DataFrame.to_dict(montecarlo[3:])
    montecarlo_dict = list(montecarlo_dict.values())
    montecarlo_list = pd.Series(montecarlo_dict[0])
    weighted_daily_return = returns_daily.mul(montecarlo_list, axis = 1)
    weighted_daily_return = weighted_daily_return.dropna()
    portfolio_daily = weighted_daily_return.sum(axis = 1)
    return portfolio_daily

def CompareToSP500(portfolio_weighted_changes, SP500_daily_returns):
    portfolio_weighted_change_df = pd.DataFrame(portfolio_weighted_change)
    portfolio_weighted_change_df['SPY'] = SP500_daily_returns
    portfolio_weighted_change_df = portfolio_weighted_change_df.dropna()
    slope, intercept, r_value, p_value, std_err = stats.linregress(portfolio_weighted_change_df['SPY'][1:], portfolio_weighted_change_df[0][1:])    
    return slope, intercept, r_value, p_value, std_err

def SP500SharpeRatio(SP500_clean):
    global SP500_daily_returns
    SP500_daily_returns = SP500_clean.pct_change()*100
    SP500_daily_returns = SP500_daily_returns.dropna()
    SP500_daily_std = SP500_daily_returns.std()
    SP500_volatility = SP500_daily_std * (252**0.5)
    SP500_first_date = SP500_clean.index[0]
    SP500_last_date = SP500_clean.index[-1]
    d1SP = pd.to_datetime(SP500_first_date)
    d2SP = pd.to_datetime(SP500_last_date)
    date_difference_SP = abs((d2SP-d1SP).days)
    years_SP = date_difference_SP/365
    SP_fractional_change = SP500_clean.iloc[-1, :] / SP500_clean.iloc[0, :]
    SP500_annual_percent_change = ((SP_fractional_change**(1/years_SP))-1)*100
    SP500_sharpe = (SP500_annual_percent_change.iloc[0]-risk_free_rate)/SP500_volatility[0]
    SP500_sharpe = pd.Series(SP500_sharpe, index={'SPY'})
    SP500_values = {'Annual % Change': SP500_annual_percent_change,
                'Volatility': SP500_volatility,
                'Sharpe Ratio': SP500_sharpe}
    SP500_df = pd.DataFrame(SP500_values)
    return SP500_df

def GetTickerData(tickers=[]):
    get_tickers = pdr.get_data_yahoo(tickers, start='01-01-1970')
    get_tickers = get_tickers['Adj Close']
    get_tickers = get_tickers.dropna()
    return get_tickers

def GetSPY():
    SPY = pdr.get_data_yahoo('SPY', start = '01-01-1970')
    SPY = SPY['Adj Close']
    SPY = SPY.dropna()
    return SPY

def CleanData(full_data, SP500, SP500_clean):
    full_data['SPY_added'] = SP500
    full_data = full_data.dropna()
    returns_daily = full_data[tickers].pct_change()*100
    returns_daily = returns_daily.dropna()
    full_data_first_date = full_data.index[0]
    full_data_last_date = full_data.index[-1]
    d1 = pd.to_datetime(full_data_first_date)
    d2 = pd.to_datetime(full_data_last_date)
    SP500_clean['SPY'] = full_data['SPY_added']
    SP500_clean = SP500_clean[d1:d2]
    SP500_clean = pd.DataFrame(SP500_clean)
    SP500_clean = SP500_clean.sort_values(by='Date')
    full_data = full_data.drop(columns=['SPY_added'])
    full_data = full_data[tickers]
    full_data = full_data.sort_values(by='Date')
    return full_data, returns_daily, SP500_clean, d1, d2

def PortfolioAnnualPercentChange(full_data):
    date_difference = abs((d2-d1).days)
    years = date_difference/365
    Total_fractional_change = (full_data.iloc[-1, :] / full_data.iloc[0, :])
    Total_fractional_change = pd.DataFrame.from_dict(Total_fractional_change)
    Total_fractional_change = Total_fractional_change.rename(columns = {0: 'Total % Change'})
    annual_percent_change = ((Total_fractional_change**(1/years))-1)*100
    return annual_percent_change

zero = time.time()
SP500_clean = pd.DataFrame()
risk_free_rate = 2.36

tickers = sys.argv[1]

full_data = GetTickerData(tickers)
SP500 = GetSPY()
full_data, returns_daily, SP500_clean, d1, d2 = CleanData(full_data, SP500, SP500_clean)
annual_percent_change = PortfolioAnnualPercentChange(full_data)
montecarlo = MonteCarlo(tickers)
#print("Dates Sampled From", d1.date(), 'To', d2.date())
#print(montecarlo)
montecarlo_JSON = MonteCarloToJSON(montecarlo, tickers)
SP500_df = SP500SharpeRatio(SP500_clean)
#print('SP500 Data \n', SP500_df.T)
portfolio_weighted_change = PortfolioChange(returns_daily, montecarlo)
slope, intercept, r_value, p_value, std_err = CompareToSP500(portfolio_weighted_change, SP500_daily_returns)
#print('R^2 value:', r_value**2)
#print('Code Execution Time:', time.time()-initial_time)
print(montecarlo_JSON)
sys.stdout.flush()
