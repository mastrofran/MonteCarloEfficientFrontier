import config
import quandl as q
import pandas as pd


def getAdjClosingPrices(tickerSymbols=["GOOG", "TSLA", "AAPL"], startDate='2016-01-01', endDate=None):

    quandlLookupSymbols = ["WIKI/" + tickerSym + ".11" for tickerSym in tickerSymbols]
    q.ApiConfig.api_key = config.quandlAPIKey
    adjClosingPrices = q.get(quandlLookupSymbols, start_date=startDate, end_date=endDate, transform="adj_close")
    adjClosingPrices.columns = tickerSymbols
    return adjClosingPrices



def getPercentReturnFromStartDate(stockPrices):
    '''
        Params:
            stockPrices - pandasDataFrame of stock prices across time.
                          Columns: Different Stocks
                          Rows: Different Time Periods
    '''

    prices = stockPrices.values
    startPrices = prices[0]
    percentReturnFromStartDate = ((prices - startPrices) / startPrices) * 100
    return pd.DataFrame(percentReturnFromStartDate, stockPrices.index, stockPrices.columns)
