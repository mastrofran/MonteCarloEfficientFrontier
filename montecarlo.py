import numpy as np
import pandas as pd

def monteCarloPortfolioSim(stocks, numOfPortfolios = 5000):
    '''
        Params:
            stocks - A pandas dataframe of stock prices across time

        Returns:
            A pandas dataframe where each row is a random portfolio and the
            columns are the weights, expected return, volatility
            and sharpe ratio
    '''

    portfolioWeights = generateRandomPortfolioWeights(numOfPortfolios, len(stocks.columns))
    expectedPortfolioReturns = getExpectedPortfolioReturns(stocks, portfolioWeights)
    expectedPortfolioVols = getExpectedPortfolioVolatility(stocks, portfolioWeights)

    portfolioDataFrame = pd.DataFrame(portfolioWeights, columns = stocks.columns)
    portfolioDataFrame['Expected Return'] = expectedPortfolioReturns
    portfolioDataFrame['Volatility'] = expectedPortfolioVols
    return portfolioDataFrame




def generateRandomPortfolioWeights(numOfPortfolios, numOfAssets):

    randWeightCoefs = np.random.rand(numOfPortfolios, numOfAssets)
    portfolioCoefSums = np.sum(randWeightCoefs, axis=1).reshape(numOfPortfolios, 1)
    normalizedRandomWeights = randWeightCoefs / portfolioCoefSums
    return normalizedRandomWeights





def getExpectedPortfolioReturns(stockPrices, portfolioWeights):
    '''
        Params:
            stocks - pandas dataframe of stock prices where Columns
                    represent the different stocks and the Rows
                    are different time periods

            portfolio weights - numpy 2d array of weights for stock prices
                                where columns represent the different stocks
                                and the rows specify the portfolios

        Returns:
            numpy array of expected portfolio returns with shape (Number of Portfolios, 1)
    '''
    percentReturns = stockPrices.pct_change().dropna().values
    averageReturns = np.mean(percentReturns, axis=0).reshape(-1,1)
    expectedPortfolioReturn = np.dot(portfolioWeights, averageReturns)
    return expectedPortfolioReturn




def getExpectedPortfolioVolatility(stockPrices, portfolioWeights):
    '''
        Params:
            stockPrices - pandas dataframe of stock prices where Columns
                    represent the different stocks and the Rows
                    are different time periods

            portfolioWeights - numpy 2d array of weights for stock prices
                                where columns represent the different stocks
                                and the rows specify the portfolios

            Returns:
                numpy array of expected portfolio volatility with shape(Number of Portfolios, 1)

    '''

    covariances = stockPrices.pct_change().dropna().cov().values
    portfolioVols = np.sum(np.dot(portfolioWeights,covariances) * portfolioWeights, axis=1)
    newVols = np.sqrt(portfolioVols)
    return newVols
