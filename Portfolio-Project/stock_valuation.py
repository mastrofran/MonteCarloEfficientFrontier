# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 17:42:29 2018

@author: Francesco
"""
from yahoofinancials import YahooFinancials
import pandas as pd
import time

initialtime=time.time()

def summary_data(ticker):
#    summary_data_list = []
#    for ticker in tickers:
    yahoo_financials = YahooFinancials(ticker)
    ass = yahoo_financials.get_summary_data(reformat=True)
    summary_data = pd.DataFrame.from_dict(ass).T
#        summary_data_list.append(summary_data)
    return summary_data
#    return summary_data_df

#def stock_valuation(tickers=[]):
#    df = []
#    for ticker in tickers:
#        global yahoo_financials 
#        yahoo_financials = YahooFinancials(ticker)
#        EPS = yahoo_financials.get_earnings_per_share()
#        price = yahoo_financials.get_current_price()
#        Market_Cap = yahoo_financials.get_market_cap()
#
#        if EPS != None:
#            PE_Ratio = price/EPS
#        else:
#            PE_Ratio = None
#        info = {'ticker': [ticker], 'Price': [price], 'EPS':[EPS], ' P/E Ratio': [PE_Ratio], 'Market_Cap ($USD)': ["{:,d}".format(Market_Cap)]}
#        info = pd.DataFrame.from_dict(info)
#        df.append(info)
#    result = pd.concat(df)
    
def stock_statements(tickers,frequency, statement_type):
#    data_list = []
#    for ticker in tickers:
    yahoo_financials = YahooFinancials(ticker)
    ass = yahoo_financials.get_financial_stmts(frequency, statement_type, reformat=True)
    if statement_type is 'cash' and frequency is 'quarterly':
        data = ass['cashflowStatementHistoryQuarterly']
    if statement_type is 'cash' and frequency is 'annual':
        data = ass['cashflowStatementHistory']
    if statement_type is 'income' and frequency is 'quarterly':
        data = ass['incomeStatementHistoryQuarterly']
    if statement_type is 'income' and frequency is 'annual':
        data = ass['incomeStatementHistory']
    if statement_type is 'balance' and frequency is 'quarterly':
        data = ass['balanceSheetHistoryQuarterly']
    if statement_type is 'balance' and frequency is 'annual':
        data = ass['balanceSheetHistory']
    return data
#        for quarter in data[ticker]:
#            data = pd.DataFrame.from_dict(quarter).T
#            data.insert(0, 'Ticker', ticker)
#            data_list.append(data)
#    data_df = pd.concat(data_list, sort=False)
#    return data_df


def claudio_ratios(ratios):
    ratios['EBIT'] = income_statement_df['netIncome']+income_statement_df['incomeTaxExpense'] - income_statement_df['interestExpense']
    ratios['EBIT Margin(%)'] = (ratios['EBIT']/income_statement_df['totalRevenue'])*100
    ratios['EBITDA'] = ratios['EBIT']+cash_statement_df['depreciation']
    ratios['EBITDA Margin(%)'] = (ratios['EBITDA']/income_statement_df['totalRevenue'])*100
    ratios['Return on Equity(%)'] = (income_statement_df['netIncome']/balance_statement_df['totalStockholderEquity'])*100
    ratios['Return on Assets(%)'] = (income_statement_df['netIncome']/balance_statement_df['totalAssets'])*100
    ratios['Profit Margin(%)'] = (income_statement_df['netIncome']/income_statement_df['totalRevenue'])*100
    ratios['Operating Margin(%)'] = (income_statement_df['operatingIncome']/income_statement_df['totalRevenue'])*100
    ratios['Gross Margin(%)'] = (income_statement_df['grossProfit']/income_statement_df['totalRevenue'])*100
    ratios['Current Ratio'] = balance_statement_df['totalCurrentAssets']/balance_statement_df['totalCurrentLiabilities']
    ratios['Quick Ratio'] = (balance_statement_df['totalCurrentAssets']-balance_statement_df['inventory'])/balance_statement_df['totalCurrentLiabilities']
    ratios['Debt-To-Assets Ratio'] = (balance_statement_df['longTermDebt'] + balance_statement_df['shortLongTermDebt'])/balance_statement_df['totalAssets']
    ratios['Debt-To-EBITDA Ratio'] = (balance_statement_df['longTermDebt'] + balance_statement_df['shortLongTermDebt'])/ratios['EBITDA']
    ratios['Interest Coverage Ratio'] = (income_statement_df['netIncome']+income_statement_df['incomeTaxExpense']-income_statement_df['interestExpense'])/(-income_statement_df['interestExpense'])
    ratios['Dividend Payout Ratio(%)'] = (cash_statement_df['dividendsPaid']/income_statement_df['netIncome'])*100
    ratios['Dividends & Share buyback / Sales'] = ((cash_statement_df['dividendsPaid'] + cash_statement_df['repurchaseOfStock'])/income_statement_df['totalRevenue'])*100
    ratios['Dividends & Share buyback / Income'] = ((cash_statement_df['dividendsPaid'] + cash_statement_df['repurchaseOfStock'])/income_statement_df['netIncome'])*100
    ratios['Dividends & Share buyback / Net CFO'] = ((cash_statement_df['dividendsPaid'] + cash_statement_df['repurchaseOfStock'])/cash_statement_df['totalCashFromOperatingActivities'])*100
    return ratios
    



tickers = ['AAPL', 'BIIB', 'FB', 'QTRX', 'SNAP', 'GE']
balance_list = []
income_list = []
cash_list = []
summary_data_list = []
for ticker in tickers:
    summary_data_df = summary_data(ticker)
    summary_data_list.append(summary_data_df)
    statement_frequency = 'annual'
    balance_statement_df = stock_statements(ticker, statement_frequency, 'balance')
    for quarter in balance_statement_df[ticker]:
        data = pd.DataFrame.from_dict(quarter).T
        data.insert(0, 'Ticker', ticker)
        balance_list.append(data)
    income_statement_df = stock_statements(ticker, statement_frequency, 'income')
    for quarter in income_statement_df[ticker]:
        data = pd.DataFrame.from_dict(quarter).T
        data.insert(0, 'Ticker', ticker)
        income_list.append(data)
    cash_statement_df = stock_statements(ticker, statement_frequency, 'cash')
    for quarter in cash_statement_df[ticker]:
        data = pd.DataFrame.from_dict(quarter).T
        data.insert(0, 'Ticker', ticker)
        cash_list.append(data)
summary_data_df = pd.concat(summary_data_list, sort=False)
summary_data_df = summary_data_df.fillna(0)
balance_statement_df = pd.concat(balance_list, sort=False)
balance_statement_df = balance_statement_df.fillna(0)
income_statement_df = pd.concat(income_list, sort=False)
income_statement_df = income_statement_df.fillna(0)
cash_statement_df = pd.concat(cash_list, sort=False)
cash_statement_df = cash_statement_df.fillna(0)
ratios=[]
ratios = pd.DataFrame(ratios)
ratios.insert(0, 'Ticker', income_statement_df['Ticker'])
claudio_ratios_df = claudio_ratios(ratios)
print(claudio_ratios_df)

finaltime = time.time()
print(finaltime - initialtime)
#yahoo_financials = YahooFinancials(tickers)
#print(yahoo_financials.get_num_shares_outstanding())
