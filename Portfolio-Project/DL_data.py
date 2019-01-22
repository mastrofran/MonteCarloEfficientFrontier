# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 16:17:49 2019

@author: Francesco
"""

import csv
import requests
import pandas as pd
from pandas_datareader import data as pdr
import os

dataframe_list = []
chunks_list = []
download = requests.get('http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=all&render=download')

with open('Tickers.csv', 'w') as file:
    writer = csv.writer(file)
    reader = csv.reader(download.text.splitlines())
    for row in reader:
        writer.writerow(row)
        
ticker_df = pd.read_csv('Tickers.csv')
IEX_tickers = pdr.get_iex_symbols()
IEX_tickers = IEX_tickers['symbol']
IEX_tickers = list(IEX_tickers)
IEX_tickers = [i.replace('-', '-P') for i in IEX_tickers]
symbols = ticker_df['Symbol']
symbols = list(symbols)
symbols = symbols + IEX_tickers
symbols = [s.replace('.', '-') for s in symbols]
symbols = [s.replace('^', '-P') for s in symbols]
symbols = list(set(symbols))
path = 'C:\\Users\Francesco\Desktop\Python_Scripts\Portfolio-Project\Stock_Data'
directory = os.listdir(path)
os.chdir(path)
directory = [s.replace('_Close.csv', '') for s in directory]
#tickers = []
stock = pd.DataFrame()
for item in symbols:
    if item not in directory:
        try:
            stock = pdr.get_data_yahoo(item, start = '01-01-1970')
            stock = stock['Adj Close']
            stock = pd.DataFrame(stock)
            stock.rename(columns={'Adj Close' : item}, inplace=True)
            stock.to_csv('%s_Close.csv'%(item))
            print('Fetched Complete Missing Stock History of', item)
        except:
            print('Could Not Fetch Complete Missing Stock History of', item)
            pass
    else:
        try:
            stock = pd.read_csv('%s_Close.csv'%(item))
            stock = stock.sort_values(by='Date')
            stock_update = pdr.get_data_yahoo(item, start = stock.iloc[-1][0])
            stock_update = stock_update.sort_values(by='Date')
            stock_update = stock_update[['Close', 'Adj Close']]
            stock_update = stock_update.drop_duplicates()
            stock_update = pd.DataFrame(stock_update)
            if (stock_update.iloc[0]['Close'] == stock_update.iloc[0]['Adj Close']) == True:
                if len(stock_update) > 1:
                    stock_update = stock_update[1:]
                    stock_update.rename(columns={'Adj Close' : item}, inplace=True)
                    stock_update = stock_update[item]
                    stock_update = pd.DataFrame(stock_update)
                    stock_update.index = stock_update.index.date
                    stock = stock.set_index('Date')
                    stock_combined = pd.concat([stock, stock_update])
                    stock_combined.to_csv('%s_Close.csv'%(item))
                    print('Ticker Updated:', item)
                else:
                    print("Ticker Doesn't Need To Be Updated:", item)
            else:
                stock_update = pdr.get_data_yahoo(item, start = '01-01-1970')
                stock_update = stock_update['Adj Close']
                stock_update = pd.DataFrame(stock_update)
                stock_update.rename(columns={'Adj Close' : item}, inplace=True)
                stock_update.to_csv('%s_Close.csv'%(item))
                print('Dividend or Stock Split Detected...Updated:', item)
        except:
            print('Tried to Update Ticker But Failed:', item)