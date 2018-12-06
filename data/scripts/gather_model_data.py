import csv   
import json
import os
import requests
import time



def get_stock_data(symbol, time='TIME_SERIES_DAILY'):
    
    payload = {'function':time,
            'symbol':symbol, 
            'outputsize':'full',
            'apikey':'V25VXU9H1BTNXDYY'}

    r = requests.get('https://www.alphavantage.co/query?', params=payload)
    responses = r.json()
    print(responses)
    file_dir = os.path.dirname(os.path.realpath('__file__'))

    print('Gathering data for '+symbol)

    for name, dictionary in responses.iteritems():
        
        if "Series" in name:
            with open(os.path.join(file_dir, '../'+symbol+'.csv'), 'w') as f:
                writer = csv.writer(f)

                #write header
                fields=['date', 'open', 'close', 'high', 'low', 'volume']
                writer.writerow(fields)

                for date, data in dictionary.iteritems():
                    fields=[date, data['1. open'], data['4. close'], data['2. high'], data['3. low'], data['5. volume']]
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

    print('Gathering data for '+symbol)

    for name, dictionary in responses.iteritems():
        
        if "Series" in name:
            with open(os.path.join(file_dir, '../'+symbol+'.csv'), 'w') as f:
                writer = csv.writer(f)
                
                #write header
                fields=['date', 'open_cny', 'open_usd', 'close_cny', 'close_usd', 'high_cny', 'high_usd', 'low_cny', 'low_usd', 'volume', 'marketcap_USD']
                writer.writerow(fields)

                for date, data in dictionary.iteritems():
                    fields=[date, data['1a. open (CNY)'], data['1b. open (USD)'], data['4a. close (CNY)'],  data['4b. close (USD)'], data['2a. high (CNY)'], data['2b. high (USD)'], data['3a. low (CNY)'], data['3b. low (USD)'], data['5. volume'], data['6. market cap (USD)']]
                    writer.writerow(fields)
    return True

def get_fx_data(from_currency, to_currency, time='FX_DAILY'):
    
    payload = {'function':time,
            'from_symbol': from_currency,
            'to_symbol':to_currency, 
            'outputsize':'full',
            'apikey':'V25VXU9H1BTNXDYY'}

    r = requests.get('https://www.alphavantage.co/query?', params=payload)
    responses = r.json()

    file_dir = os.path.dirname(os.path.realpath('__file__'))

    print('Gathering data for '+ from_currency+' --> '+to_currency)

    for name, dictionary in responses.iteritems():
        
        if "Series" in name:
            with open(os.path.join(file_dir, '../'+from_currency+to_currency+'.csv'), 'w') as f:
                writer = csv.writer(f)
                
                #write header
                fields=['date', 'open', 'high', 'low', 'close']
                writer.writerow(fields)

                for date, data in dictionary.iteritems():
                    fields=[date, data['1. open'], data['2. high'], data['3. low'],  data['4. close']]
                    writer.writerow(fields)
    return True


if __name__ == '__main__':
    #gather crypto data
    get_crypto_data('BTC')
    time.sleep(12)

    #gather fx data
    get_fx_data('CNY', 'USD')
    time.sleep(12)
    get_fx_data('RUB', 'USD')
    time.sleep(12)
    get_fx_data('INR', 'USD')
    time.sleep(12)

    #gather stock data
    get_stock_data('EGO') #Eldorado Gold Corp
    time.sleep(12)
    get_stock_data('AU')  #AngloGold Ashnati
    time.sleep(12)
    get_stock_data('SLW') #Silver Wheaton Corp
    time.sleep(12)
    get_stock_data('ABX') #Barrick Gold Corp
    time.sleep(12)
    get_stock_data('BVN') #Compania de Minas Buenaventura