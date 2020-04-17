import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr

folder = "/home/westy/Source/FinancePython/src/tf/"
# Dow Jones 30
#symbols_table = pd.read_html("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average#constituents",header=0)[2]
symbols_table = pd.read_csv(folder + "symbols.csv")
symbols = list(symbols_table.loc[:, "Symbol"])
index_symbol = ['^DJI']
# Dates
start_date = '2008-01-01'
end_date = '2020-03-31'

# Download the data
data = pd.DataFrame()
# Clean all symbol labels and remove unavailable ones
for i in range(len(symbols)):
    symbols[i]=symbols[i].replace(u'\xa0',u'').replace("NYSE:","")
#symbols.remove('DOW') # DOW data are unvailable on yahoo

for i in range(len(symbols)):
    print('Downloading.... ', i, symbols[i])
# User pandas_reader.data.DataReader to load the desired data.
# As simple as that.
    data[symbols[i]] = pdr.DataReader(symbols[i], "yahoo",start_date, end_date)['Adj Close']

data_index = pdr.DataReader(index_symbol, "yahoo", start_date, end_date)['Adj Close']

# Remove the missing the data from the dataframe
data = data.dropna()
data_index = data_index.dropna()

# Save the data
data.to_csv(folder + 'dj30_10y.csv', sep=',', encoding='utf-8')
data_index.to_csv(folder + 'dj30_index_10y.csv', sep=',', encoding='utf-8')
print(data.head())


