client_id = 'api_key'
secret_key = 'secret-key'
redirect_uri = 'https://api.upstox.com/v2/login' # if you are using upstox account 

url = f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"

print("Hit the URL and type the PIN and get the code in URL, This code changes everytime you hit it",url)

#-----------------------------------------------------------------------------------------------------------------------------------

code = "copy this code from URL"  # Once you run the above URL get the code here

#########################################################################

import requests

url = 'https://api.upstox.com/v2/login/authorization/token'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
    'code': code,
    'client_id': client_id,
    'client_secret': secret_key,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code',
}

response = requests.post(url, headers=headers, data=data)

print(response.status_code)
print(response.json())

access_token = response.json()['access_token']

#-----------------------------------------------------------------------------------------------------------------------------------
#Check the data response

import requests

url = 'https://api.upstox.com/v2/historical-candle/NSE_INDEX|Nifty 50/1minute/2024-05-31/2024-05-30'
headers = {
    'Accept': 'application/json'
}

response = requests.get(url, headers=headers)

# Check the response status
if response.status_code == 200:
    # Do something with the response data (e.g., print it)
    print(response.json())
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.text}")

#-----------------------------------------------------------------------------------------------------------------------------------
# Below script is to download the data 

import requests
import csv
from datetime import datetime

url = 'https://api.upstox.com/v2/historical-candle/NSE_EQ|INE522F01014/day/2024-12-30/2005-01-01' # Instrument name should be correct data order = greater, smaller
headers = {
    'Accept': 'application/json'
}

response = requests.get(url, headers=headers)

# Check the response status
if response.status_code == 200:
    data = response.json()['data']['candles']
    print(response.json())
    
    # Extract the timestamps
    timestamps = [candle[0] for candle in data]
    
    # Convert timestamps to datetime objects
    datetime_objects = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps]
    
    # Find the min and max dates
    min_date = min(datetime_objects)
    max_date = max(datetime_objects)
    
    # Print the min and max dates
    print(f"Min date: {min_date}")
    print(f"Max date: {max_date}")
    
    # Define the CSV file name
    csv_file = 'output.csv'
    
    # Write data to CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow(['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover'])
        
        # Write data
        for candle in data:
            writer.writerow(candle)
    
    print(f"Data successfully exported to {csv_file}")
else:
    print(f"Error: {response.status_code} - {response.text}")

#--------------------------------------------------------------------------------------------------
# use below code to plot the candlestick chart for the downloaded data

import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# Read data from CSV file
csv_file = 'output.csv'
df = pd.read_csv(csv_file, parse_dates=['Timestamp'], index_col='Timestamp')

# Resample to 5-minute intervals
df_5min = df.resample('5T').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume': 'sum',
    'Turnover': 'sum'
}).dropna()

# Calculate 9-period and 21-period EMA
df_5min['9EMA'] = df_5min['Close'].ewm(span=9, adjust=False).mean()
df_5min['21EMA'] = df_5min['Close'].ewm(span=21, adjust=False).mean()

# Visualize data in candlestick form
apds = [
    mpf.make_addplot(df_5min['9EMA'], color='blue'),
    mpf.make_addplot(df_5min['21EMA'], color='red')
]

# Plot with mplfinance and set plot size
mpf.plot(df_5min, type='candle', style='charles', addplot=apds, figsize=(15, 7), title='5-Minute Candlestick Chart with EMAs', ylabel='Price')

plt.show()

#-----------------------------------------End of Script---------------------------------------------------------------------------------------

