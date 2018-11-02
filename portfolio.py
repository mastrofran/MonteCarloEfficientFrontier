import numpy as np

def adjustTimePeriod(portfolios, timePeriod):
    '''
        Params:
            portfolios - A pandas dataframe of the portfolios with a
            Expected Return, and Volatility column

            timePeriod - the number of time periods within the new time period
                        ex/ To convert from daily to annual the time period would be
                        365 (unless counting trading days)

        Returns:
            pandas dataframe with the appropriate fields adjusted
    '''
    portfolios['Expected Return'] = ((portfolios['Expected Return'].values + 1) ** timePeriod) - 1
    portfolios['Volatility'] = np.sqrt((portfolios['Volatility'] ** 2) * timePeriod)
    return portfolios
