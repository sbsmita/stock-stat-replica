import requests
import pandas as pd
import os
import numpy as np
import json
import re


cwd=os.getcwd()
url = f'https://www.alphavantage.co/query'

# Function checks if the string
# contains any special character
def string_check(string):

    # Make own character set and pass
    # this as argument in compile method
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

    # Pass the string in search
    # method of regex object.
    if(regex.search(string) == None):
        return True
    else:
        return False


def API_call(symbol, frequency='Time Series (Daily)', subfolder=''):

    cwd=os.getcwd()
    print(cwd)

    # os.chdir("..")
    cwd=os.getcwd() + '/data/'

    print(cwd)

    test_symbol = symbol

    #checking if symbol has any special strings
    if string_check(test_symbol):

        print('Calling API for ' + test_symbol)

        if frequency=='Time Series (Daily)':
            params = {
                "function" :"TIME_SERIES_DAILY",
                "symbol" : test_symbol,
                "apikey" : os.environ.get('APIKEY'),
                "outputsize" : "full",
            #     "datatype" : "csv"
            }
        else:
            print('Call abandoned. Unknown data frequency requested')

        response = requests.get(url, params=params).json()
        #print(response)
        data = response[frequency]

        df = pd.DataFrame(data).T

        if test_symbol[:-2]=='.L':
            storing_name=test_symbol[:-2]
        else :
            storing_name=test_symbol

        df.to_csv(cwd + subfolder + storing_name+'.csv')

        print(f'TIME_SERIES_DAILY of ticker {test_symbol} stored under {storing_name}.csv')
        return True

    else:
        print('Please ensure that your ticker does not include special characters')
        #test_symbol=test_symbol.replace("/","")
        print('Abandoning API Call - Please try again')

        return False

API_call('IBM')
