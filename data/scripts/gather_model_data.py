import csv   
import json
import os

import requests



def get_stock_data(symbol, time='TIME_SERIES_DAILY'):
    
    payload = {'function':time,
            'symbol':symbol, 
            'outputsize':'full',
            'apikey':'V25VXU9H1BTNXDYY'}

    r = requests.get('https://www.alphavantage.co/query?', params=payload)
    responses = r.json()

    file_dir = os.path.dirname(os.path.realpath('__file__'))

    for name, dictionary in responses.iteritems():
        print(name)
        if "Series" in name:
            for date, data in dictionary.iteritems():
                fields=[date, data['1. open'], data['4. close'], data['2. high'], data['3. low'], data['5. volume']]
                with open(os.path.join(file_dir, '../'+symbol+'.csv'), 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)
    return True

def get_crypto_data(symbol, time='DIGITAL_CURRENCY_DAILY'):
    
    payload = {'function':time,
            'market': 'CNY',
            'symbol':symbol, 
            'outputsize':'full',
            'apikey':'V25VXU9H1BTNXDYY'}

    r = requests.get('https://www.alphavantage.co/query?', params=payload)
    responses = r.json()

    file_dir = os.path.dirname(os.path.realpath('__file__'))

    for name, dictionary in responses.iteritems():
        print(name)
        if "Series" in name:
            for date, data in dictionary.iteritems():
                print(data)
                fields=[date, data['1a. open (CNY)'], data['1b. open (USD)'], data['4a. close (CNY)'],  data['4b. close (USD)'], data['2a. high (CNY)'], data['2b. high (USD)'], data['3a. low (CNY)'], data['3b. low (USD)'], data['5. volume'], data['6. market cap (USD)']]
                with open(os.path.join(file_dir, '../'+symbol+'.csv'), 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)
    return True

if __name__ == '__main__':
    get_crypto_data('BTC')