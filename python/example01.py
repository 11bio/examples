#!/usr/bin/env python3
#
#  Copyright (c) 2019, 11B.io authors, all rights reserved.
#
#
import requests 
import json
from config import config
import ssl

def print_json(parsed_json):
    print(json.dumps(parsed_json, indent=4))

headers = {
    'Authorization': 'Bearer ' + config.API_KEY,
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

if __name__ == "__main__":

    # /GET currencies
    r = requests.get(url = config.API_URL+'/api/v1/currencies',  headers=headers ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)
        raise SystemExit


    # /GET symbols
    r = requests.get(url = config.API_URL+'/api/v1/symbols',  headers=headers ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    # /GET accounts
    r = requests.get(url = config.API_URL+'/api/v1/accounts',  headers=headers ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    # /GET orders
    r = requests.get(url = config.API_URL+'/api/v1/orders',  headers=headers ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    # /GET positions
    r = requests.get(url = config.API_URL+'/api/v1/positions',  headers=headers ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    # /GET closed_positions
    r = requests.get(url = config.API_URL+'/api/v1/closed_positions',  headers=headers ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    # /POST Limit Entry
    r = requests.post(url = config.API_URL+'/api/v1/orders',  headers=headers, data = {
        'account_id': config.API_ACCOUNT,
        'order_type': "LIMIT_ENTRY",
        'symbol': "EUR/USD",
        'side': "BUY",
        'quantity': 10000,
        'price': 1.1280,
        'stop_price': 1.12,
        'limit_price': 1.15,
        'client_order_id': "order-entry_stop-buy-"+config.API_ACCOUNT        
    } ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
        limit_entry_order_id = data['order']['order_id']
    else:
        print('error', r.status_code)

    # /PATCH Limit Entry
    r = requests.patch(url = config.API_URL+'/api/v1/orders',  headers=headers, data = {
        'order_id': limit_entry_order_id,
        'price': 1.1281

    } ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)


    # /POST Limit Entry
    r = requests.delete(url = config.API_URL+'/api/v1/orders',  headers=headers, data = {
        'order_id': limit_entry_order_id
    } ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)


    # /POST Market order
    r = requests.post(url = config.API_URL+'/api/v1/orders',  headers=headers, data = {
        'account_id': config.API_ACCOUNT,
        'order_type': "MARKET",
        'symbol': "EUR/USD",
        'side': "BUY",
        'quantity': 10000,
        'price': 1.1280,
        'client_order_id': "order-market-buy-"+config.API_ACCOUNT        
    } ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
        position_id = data['positions'][0]['position_id']
    else:
        print('error', r.status_code)


    # /POST Market order
    r = requests.post(url = config.API_URL+'/api/v1/orders',  headers=headers, data = {
        'account_id': config.API_ACCOUNT,
        'order_type': "MARKET",
        'position_id': position_id,
        'symbol': "EUR/USD",
        'side': "SELL",
        'quantity': 10000,
        'price': 1.1280,
        'client_order_id': "order-market-sell-"+config.API_ACCOUNT        
    } ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    raise SystemExit

    