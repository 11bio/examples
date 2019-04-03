#!/usr/bin/env python3
#
# Copyright (c) 2019, 11B.io authors, all rights reserved.
# 
# Ordering requests examples
#

import json
import requests
import ssl
import sys

from config import config

def print_json(parsed_json):
    """PRint JSON"""

    print(json.dumps(parsed_json, indent=4))

def check_response(res):
    """Checks response for errors.
    Terminates application in case of error.
    Returns json data otherwise.
    """

    try:
        data = res.json()
    except Exception as ex:
        print(ex)
        data = None

    if res.status_code != 200 or not data or 'error' in data:
        print('Error! Status: %s; Message: %s' % (res.status_code, data.get('error')))
        if data:
            print('Response: ')
            print_json(data)
        sys.exit(1)
    return data

def main():
    headers = {
        'Authorization': 'Bearer ' + config.API_KEY,
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }


    # GET currencies
    print('\nGet Currencies: ')
    res = requests.get(url = config.API_URL + '/api/v1/currencies', headers = headers) 
    res_data = check_response(res)
    print_json(res_data)


    # GET symbols
    print('\nGet Symbols: ')
    res = requests.get(url = config.API_URL + '/api/v1/symbols', headers = headers) 
    res_data = check_response(res)
    print_json(res_data)

    # GET quotes
    print('\nGet Quotes: ')
    res = requests.get(url = config.API_URL + '/api/v1/quotes?symbols=EUR/USD,USD/JPY', headers = headers) 
    res_quotes = check_response(res)
    print_json(res_quotes)


    # GET accounts
    print('\nGet Accounts: ')
    res = requests.get(url = config.API_URL + '/api/v1/accounts', headers = headers) 
    res_data = check_response(res)
    print_json(res_data)


    # GET orders
    print('\nGet Orders: ')
    res = requests.get(url = config.API_URL + '/api/v1/orders', headers = headers) 
    res_data = check_response(res)
    print_json(res_data)


    # GET positions
    print('\nGet Positions: ')
    res = requests.get(url = config.API_URL + '/api/v1/positions', headers = headers) 
    res_data = check_response(res)
    print_json(res_data)


    # GET closed_positions
    print('\nGet Closed Positions: ')
    r = requests.get(url = config.API_URL + '/api/v1/closed_positions', headers = headers) 
    res_data = check_response(res)
    print_json(res_data)


    # Create Limit Entry
    print('\nCreate Limit Entry: ')
    params = {
        'account_id': config.API_ACCOUNT,
        'order_type': 'LIMIT_ENTRY',
        'symbol': 'EUR/USD',
        'side': 'BUY',
        'quantity': 10000,
        'price': res_quotes['quote_snapshot'][0]['offer']-.0050,
        'stop_price': res_quotes['quote_snapshot'][0]['offer']-.010,
        'limit_price': res_quotes['quote_snapshot'][0]['offer'],
        'client_order_id': 'order-limit_entry-buy-' + config.API_ACCOUNT        
    }
    res = requests.post(url = config.API_URL + '/api/v1/orders', headers = headers, data = params) 
    res_data = check_response(res)
    print_json(res_data)

    limit_entry_order_id = None
    if ('order' in res_data) and ('order_id' in res_data['order']):
        limit_entry_order_id = res_data['order']['order_id']
    print('Limit Entry Order ID: %s' % limit_entry_order_id)

    limit_order_id = None
    if ('linked_orders' in res_data) and (len(res_data['linked_orders']) > 0) and ('order_id' in res_data['linked_orders'][0]):
        limit_order_id = res_data['linked_orders'][0]['order_id']
    print('Limit Order ID: %s' % limit_order_id)


    # Change Entry Price
    print('\nChange Entry Price: ')
    params = {
        'order_id': limit_entry_order_id,
        'price':res_quotes['quote_snapshot'][0]['offer']-.0040
    }
    res = requests.patch(url = config.API_URL + '/api/v1/orders', headers = headers, data = params)
    res_data = check_response(res)
    print_json(res_data)


    # Delete Limit from Entry
    print('\nDelete Limit for Entry: ')
    params = {
        'order_id': limit_order_id
    }
    res = requests.delete(url = config.API_URL + '/api/v1/orders', headers = headers, data = params) 
    res_data = check_response(res)
    print_json(res_data)


    # Delete Limit Entry
    print('\nDelete Limit Entry: ')
    params = {
        'order_id': limit_entry_order_id
    }
    res = requests.delete(url = config.API_URL + '/api/v1/orders', headers = headers, data = params) 
    res_data = check_response(res)
    print_json(res_data)


    # Create Market order
    print('\nCreate Market Order: ')
    params = {
        'account_id': config.API_ACCOUNT,
        'order_type': 'MARKET',
        'symbol': 'EUR/USD',
        'side': 'BUY',
        'quantity': 10000,
        'price': 1.1280,
        'client_order_id': 'order-market-buy-' + config.API_ACCOUNT        
    }
    res = requests.post(url = config.API_URL + '/api/v1/orders', headers = headers, data = params) 
    res_data = check_response(res)
    print_json(res_data)

    position_id = None
    if ('positions' in res_data) and (len(res_data['positions']) > 0) and ('position_id' in res_data['positions'][0]):
        position_id = res_data['positions'][0]['position_id']        
    print('Position ID: %s' % position_id)


    # Create closing Market order
    print('\nCreate Closing Market Order: ')
    params = {
        'account_id': config.API_ACCOUNT,
        'order_type': 'MARKET',
        'position_id': position_id,
        'symbol': 'EUR/USD',
        'side': 'SELL',
        'quantity': 10000,
        'price': 1.1280,
        'client_order_id': 'order-market-sell-' + config.API_ACCOUNT        
    }
    res = requests.post(url = config.API_URL + '/api/v1/orders', headers = headers, data = params)
    res_data = check_response(res)
    print_json(res_data)


    # Successfully Finished
    return 0

if __name__ == '__main__':
    sys.exit(main())
