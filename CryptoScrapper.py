# Importing the necessary libraries
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# Defining the API endpoint URL 
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' 
#Original Sandbox Environment: 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

#  setting the required parameters and headers for the request.
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'YOUR_API_KEY_HERE',
}

# Initiating a session and updating the session headers with the specified headers
session = Session()
session.headers.update(headers)

# Sending a GET request to the API endpoint using the session and parameters.
try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  #print(data)
  
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# Here we export the data into pandas dataframe for analysis & visualization
import pandas as pd


# This allows you to see all the columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# This normalizes the data and makes it all pretty in a dataframe
df = pd.json_normalize(data['data'])

# Create a column to know what time each process ran successfully at continuous call
df['timestamp'] = pd.to_datetime('now', utc=True)
df

# Creating a function to automate the data retrieval process
def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' 
    parameters = {
      'start':'1',
      'limit':'15',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'YOUR_API_KEY_HERE',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

    
    # Adding to an existing dataframe
    df2 = pd.json_normalize(data['data'])
    df2['Timestamp'] = pd.to_datetime('now', utc=True)
    #df = df.append(df2)    has been deprecated
    df = pd.concat([df, df2])


    #Creating a csv and appending the data into it
    df = pd.json_normalize(data['data'])
    df['timestamp'] = pd.to_datetime('now', utc=True)
    #print(df)
    if not os.path.isfile(r'YOUR_FILE_PATH_HERE'):
      df.to_csv(r'YOUR_FILE_PATH_HERE', header='column_names')
    else:
      df.to_csv(r'YOUR_FILE_PATH_HERE', mode='a', header=False)
        
    #Then to read in the file: df = pd.read_csv(r'YOUR_FILE_PATH_HERE')



import os 
from time import time
from time import sleep

for i in range(333):
    api_runner()
    print('API Runner completed')
    sleep(250) #sleep for some minutes
exit()


df72 = pd.read_csv(r'YOUR_FILE_PATH_HERE')
#print(df72)

# Formatting response numbers with exponential format
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Now let's look at the coin trends over time

df3 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean()
#print(df3)

df4 = df3.stack()
#print(df4)

type(df4)

# Converting stack to frame
df5 = df4.to_frame(name='values')
#print(df5)

df5.count()


index = pd.Index(range(90))

# Set the above DataFrame index object as the index
# using set_index() function
df6 = df5.set_index(index)
#print(df6)

# If it only has the index and values try doing reset_index like "df5.reset_index()"


# Change the column name

df7 = df6.rename(columns={'level_1': 'percent_change'})
#print(df7)

df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d'],['24h','7d','30d','60d','90d'])
#print(df7)

# Creating visuals for the data
import seaborn as sns
import matplotlib.pyplot as plt

sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')

df8 = df[['name','quote.USD.price','timestamp']]
df8 = df8.query("name == 'Bitcoin'")
#print(df8)

sns.set_theme(style="darkgrid")

sns.lineplot(x='timestamp', y='quote.USD.price', data = df8)