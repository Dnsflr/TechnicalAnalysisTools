import yfinance as yf
import matplotlib.pyplot as plt

# Defining companies
orlen = 'PKN.WA'
cdprojekt = 'CDR.WA'

# Downloading data with weekly interval from August 15, 2021 to January 1, 2024
start_date = "2021-08-15"
end_date = "2024-01-01"

orlen_data = yf.download(orlen, start=start_date, end=end_date, interval='1wk')
cdprojekt_data = yf.download(cdprojekt, start=start_date, end=end_date, interval='1wk')

# Calculating Bollinger Bands
def calculate_bollinger_bands(data, window=20):
    data['SMA'] = data['Close'].rolling(window).mean()
    data['STD'] = data['Close'].rolling(window).std()
    data['Upper Band'] = data['SMA'] + (data['STD'] * 2)
    data['Lower Band'] = data['SMA'] - (data['STD'] * 2)
    return data

orlen_data = calculate_bollinger_bands(orlen_data)
cdprojekt_data = calculate_bollinger_bands(cdprojekt_data)

# Filtering data for the period from January 1, 2022 to January 1, 2024
orlen_data_filtered = orlen_data.loc["2022-01-01":"2024-01-01"]
cdprojekt_data_filtered = cdprojekt_data.loc["2022-01-01":"2024-01-01"]

# Saving data to CSV files
orlen_data_filtered.to_csv('orlen_bollinger_filtered.csv')
cdprojekt_data_filtered.to_csv('cdprojekt_bollinger_filtered.csv')

# Plots for ORLEN
plt.figure(figsize=(14, 10))

# Plotting stock prices with Bollinger Bands
plt.plot(orlen_data_filtered.index, orlen_data_filtered['Close'], label='Close Price', color='black')
plt.plot(orlen_data_filtered.index, orlen_data_filtered['SMA'], label='20-Week SMA', color='blue')
plt.plot(orlen_data_filtered.index, orlen_data_filtered['Upper Band'], label='Upper Band', color='red')
plt.plot(orlen_data_filtered.index, orlen_data_filtered['Lower Band'], label='Lower Band', color='red')
plt.fill_between(orlen_data_filtered.index, orlen_data_filtered['Upper Band'], orlen_data_filtered['Lower Band'], color='grey', alpha=0.3)

plt.title('ORLEN - Stock Prices and Bollinger Bands')
plt.legend(loc='best')
plt.show()

# Plots for CD PROJEKT
plt.figure(figsize=(14, 10))

# Plotting stock prices with Bollinger Bands
plt.plot(cdprojekt_data_filtered.index, cdprojekt_data_filtered['Close'], label='Close Price', color='black')
plt.plot(cdprojekt_data_filtered.index, cdprojekt_data_filtered['SMA'], label='20-Week SMA', color='blue')
plt.plot(cdprojekt_data_filtered.index, cdprojekt_data_filtered['Upper Band'], label='Upper Band', color='red')
plt.plot(cdprojekt_data_filtered.index, cdprojekt_data_filtered['Lower Band'], label='Lower Band', color='red')
plt.fill_between(cdprojekt_data_filtered.index, cdprojekt_data_filtered['Upper Band'], cdprojekt_data_filtered['Lower Band'], color='grey', alpha=0.3)

plt.title('CD PROJEKT - Stock Prices and Bollinger Bands')
plt.legend(loc='best')
plt.show()