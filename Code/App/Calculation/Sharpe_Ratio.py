import pandas as pd
import numpy as np

# Purpose: To calculate the sharpe ratio of each stock

# VALUES
# Risk free rate of 5 yrs from US Treasury in %
risk_free_rate = 2.74
# 2018 inflation rate in %
inflation_rate = 1.9

# Load the datasets
df_stats = pd.read_csv('../../../Dataset_clean/stats_UtoD.csv')
df_stats = df_stats.drop(['Unnamed: 0'], axis = 1)
df_price = pd.read_csv('../../../Dataset_clean/price_UtoD.csv')
df_price = df_price.drop(['Unnamed: 0'], axis = 1)

# Declare Dataframe
df_value = pd.DataFrame(columns = ['Ticker', 'Expected_Annual_Return', 'Stock_Volatility', 'Sharpe_Ratio'])
df_test = []

# To count the rows in the dataframe
index = 0
for stock in df_price['symbol'].unique():
    df_filter = df_price[df_price['symbol'] == stock].copy()

    # SHARPE RATIO
    # Calculate Expected Annual Return
    df_filter['Daily_Return'] = df_filter.close.diff()
    expected_annual_return = (df_filter['Daily_Return'].sum()/df_filter['Daily_Return'].size * 252)
    # Calculate Annualized Standard Deviation
    std = np.std(df_filter['Daily_Return'])*np.sqrt((252))
    # Sharpe Ratio of a stock
    sharpe_ratio = ((expected_annual_return - (risk_free_rate - inflation_rate)) / std).round(4)

    df_value.loc[index, ['Ticker']] = stock
    df_value.loc[index, ['Expected_Annual_Return']] = expected_annual_return.round(4)
    df_value.loc[index, ['Stock_Volatility']] = std.round(4)
    df_value.loc[index, ['Sharpe_Ratio']] = sharpe_ratio

    index += 1

df_value = df_value.sort_values(by=['Ticker']).reset_index(drop = True)

# To load Beta from df_stats to df_result
index = 0
for stock in df_stats['Ticker'].unique():
    df_filter2 = df_stats[df_stats['Ticker'] == stock].copy()
    df_filter2 = df_filter2[['Ticker', 'Beta']].dropna().tail(1)
    df_test.append(df_filter2)
    index += 1

df_test = pd.concat(df_test)
df_test = df_test.reset_index(drop = True)
df_result = pd.concat([df_value, df_test], axis = 1)
# Drop duplicated column
df_result = df_result.loc[:, ~df_result.columns.duplicated()]

market_return = df_result['Expected_Annual_Return'].sum() / df_result['Expected_Annual_Return'].size


# RISK-FREE RETURN BY CAPITAL ASSET PRICING MODEL
df_result['Risk_Free_Return'] = (risk_free_rate + df_result['Beta'] * (market_return - risk_free_rate)).round(4)



# Calculate the Standard Deviation of the porfolio



df_result.to_csv('../../../Dataset/value.csv')

#df_price_ABT.to_csv('F:/Users/Google Drive/Graduate Diploma/Continuing Education/CEBD 1260/Project/Dataset/ABT.csv')