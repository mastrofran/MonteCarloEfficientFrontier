import stocks
import montecarlo
import portfolios

# How to get adjusted closing prices
adjClosingPrices = stocks.getAdjClosingPrices()

# If you want to see it as a percent return from start date you can call the method:
percentReturn = stocks.getPercentReturnFromStartDate(adjClosingPrices)


### Monte Carlo Simulation
portfolios = montecarlo.monteCarloPortfolioSim(adjClosingPrices)

# To adjust the returns and volatility to an annual period use:
annualizedPortfolios = portfolio.adjustTimePeriod(portfolios, 251)
print(annualizedPortfolios)
