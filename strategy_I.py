import pandas as pd
import numpy as np
import os


def list_of_ticker(tickers):  # list of tickers
    directory = 'C:\\Users\\m_met\\OneDrive\\Pulpit\\projekt giełda\\companies AT signals'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            tickers.append(filename)
    return tickers


def custom_tickers(ticker):
    company = 'C:\\Users\\m_met\\OneDrive\\Pulpit\\projekt giełda\\companies AT signals\\' + ticker
    infile = open(company, 'r')
    df = pd.read_csv(company)
    infile.close()
    df = df.drop(df.columns[[0]], axis=1)

    interval = 30
    vol = np.array(df['volume'][-interval:])
    price = np.array(df['close'][-interval:])
    np.set_printoptions(suppress=True)
    avg_price = np.round(np.sum(price), decimals=2)/interval
    avg_vol = np.round(np.sum(vol), decimals=2)/interval

    stock_turnover = round(avg_vol*avg_price, 2)

    return stock_turnover, df


def list_of_custom_tickers(list_of_tickers):
    filtered_tickers = []
    for ticker in list_of_tickers:
        stock_turnover = custom_tickers(ticker)[0]
        if stock_turnover > 100000:
            filtered_tickers.append(ticker)
    return filtered_tickers


def return2(lf, rest, data_return):
    min_index = rest['buy date'].idxmin()
    roi = rest['sell price'][min_index] / rest['buy price'][min_index]
    sell_buy = (rest['ticker'][min_index], rest['buy date'][min_index], rest['buy price'][min_index], rest['sell date'][min_index], rest['sell price'][min_index], roi)
    data_return.append(sell_buy)
    lf['control'][min_index] = 1
    return lf, data_return


def return1(lf):
    data_return = []
    lf['control'] = 0
    for i in range(len(lf)):
        rest = lf.loc[lf['control'] == 0]
    return lf


def strategy(df, ticker):
    for i in range(len(df)):
        if df['SMA_signal'][i] == 'buy' and df['MACD_trend'][i] == 'uptrend' and df['AD_long'][i] == 'buy' and df['OBV_long'][i] == 'buy':
            for k in range(i, len(df)):
                if df['SMA_signal'][k] == 'sell':
                    sell_buy = (ticker, 'buy', df['date'][i], round(df['close'][i], 2), 'sell', df['date'][k], round(df['close'][k], 2))
                    data.append(sell_buy)
                    break
                elif k == len(df) - 1:
                    sell_buy = (ticker, 'buy', df['date'][i], round(df['close'][i], 2), 'sell', df['date'][k], round(df['close'][k], 2))
                    data.append(sell_buy)
                    break
    return data


def data_frame(filtered_tickers):
    for ticker in filtered_tickers:
        df = custom_tickers(ticker)[1]
        strategy(df, ticker)

    lf = pd.DataFrame(data)
    lf.columns = ['ticker', 'buy', 'buy date', 'buy price', 'sell', 'sell date', 'sell price']
    lf['return'] = round(lf['sell price'] / lf['buy price'] -1, 2)
    return lf


data = []
tickers = []
list_of_tickers = list_of_ticker(tickers)
filtered_tickers = list_of_custom_tickers(list_of_tickers)
print(filtered_tickers)

lf = data_frame(filtered_tickers)
print(lf)

avg_return = lf['return'].sum() / len(lf)
print(avg_return)

#total_return = 1
#total_return = (lf['sell price'].sum() - lf['buy price'].sum()) / lf['buy price'].sum()

#for i in range(5):
#    if lf['return'][i] != 0:
#        total_return = total_return * lf['return'][i]

#print("total return in period ", round(total_return, 2))

base_filename = 'strategy I.txt'
with open(os.path.join('C:\\Users\\m_met\\OneDrive\\Pulpit\\projekt giełda\\strategies', base_filename), 'w') as outfile:
    lf.to_string(outfile)