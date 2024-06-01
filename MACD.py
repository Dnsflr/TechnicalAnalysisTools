import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Defining companies
orlen = 'PKN.WA'
cdprojekt = 'CDR.WA'

# Downloading data with weekly interval
orlen_data = yf.download(orlen, start="2022-01-01", end="2024-01-01", interval='1wk')
cdprojekt_data = yf.download(cdprojekt, start="2022-01-01", end="2024-01-01", interval='1wk')


# Calculating MACD and signal line
def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    ema_fast = data['Close'].ewm(span=fast_period, adjust=False).mean()
    ema_slow = data['Close'].ewm(span=slow_period, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, macd_signal


# Adding crossing signals
def find_crossings(macd, macd_signal):
    crossings = ((macd > macd_signal) & (macd.shift(1) <= macd_signal.shift(1))) | \
                ((macd < macd_signal) & (macd.shift(1) >= macd_signal.shift(1)))
    return crossings


# Process data for ORLEN
orlen_data['MACD'], orlen_data['MACD_Signal'] = calculate_macd(orlen_data)
orlen_data['Crossing'] = find_crossings(orlen_data['MACD'], orlen_data['MACD_Signal'])
orlen_crossings = orlen_data[orlen_data['Crossing']]

# Process data for CD PROJEKT
cdprojekt_data['MACD'], cdprojekt_data['MACD_Signal'] = calculate_macd(cdprojekt_data)
cdprojekt_data['Crossing'] = find_crossings(cdprojekt_data['MACD'], cdprojekt_data['MACD_Signal'])
cdprojekt_crossings = cdprojekt_data[cdprojekt_data['Crossing']]


# Printing stock prices at MACD signal line crossings
def print_crossing_prices(crossings, stock_name):
    print(f"Stock prices for {stock_name} at MACD signal line crossings:")
    for date, price in zip(crossings.index, crossings['Close']):
        print(f"Date: {date}, Price: {price}")


print_crossing_prices(orlen_crossings, 'ORLEN')
print_crossing_prices(cdprojekt_crossings, 'CD PROJEKT')

# Saving data to CSV files
orlen_data.to_csv('orlen_macd.csv')
cdprojekt_data.to_csv('cdprojekt_macd.csv')


# Plotting function
def plot_macd(data, crossings, stock_name):
    plt.figure(figsize=(14, 10))

    # Plotting the closing prices with MACD crossings
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(data.index, data['Close'], label='Close Price', color='black')
    ax1.scatter(crossings.index, crossings['Close'], marker='o', color='purple', label='MACD Crossings')
    ax1.set_title(f'{stock_name} - Stock Prices and MACD Lines')
    ax1.legend(loc='best')

    # Plotting the MACD and Signal Line on the same axis
    ax2 = ax1.twinx()
    ax2.plot(data.index, data['MACD'], label='MACD', color='blue', linestyle='--')
    ax2.plot(data.index, data['MACD_Signal'], label='Signal Line', color='red', linestyle='--')
    ax2.axhline(0, color='gray', linewidth=0.5, linestyle='--')
    ax2.legend(loc='upper left')

    # Plotting the MACD and Signal Line separately
    plt.subplot(2, 1, 2)
    plt.plot(data.index, data['MACD'], label='MACD', color='blue')
    plt.plot(data.index, data['MACD_Signal'], label='Signal Line', color='red')
    plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
    plt.title(f'{stock_name} - MACD')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.show()


# Plotting for ORLEN
plot_macd(orlen_data, orlen_crossings, 'ORLEN')

# Plotting for CD PROJEKT
plot_macd(cdprojekt_data, cdprojekt_crossings, 'CD PROJEKT')