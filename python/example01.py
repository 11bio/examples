#!/usr/bin/env python3
#
#  Copyright (c) 2019, 11B.io authors, all rights reserved.
#
#



import requests 
import json
from config import config
import websocket
import ssl

try:
    import thread
except ImportError:
    import _thread as thread
import time

headers = {
    'Authorization': 'Bearer ' + config.api_key,
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

def on_message(ws, message):
    print('on_mesage', message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def run(*args):
    while True:
        time.sleep(1)

def on_open(ws):
    ws.send(json.dumps({'type': 'subscribe', 'symbols': [
        { 'symbol': 'EUR/USD', 'level': 1 },
        { 'symbol': 'USD/JPY', 'level': 1 },
        { 'symbol': 'GBP/USD', 'level': 1 },
        { 'symbol': 'ETH/USD', 'level': 1 },
        { 'symbol': 'BTC/USD', 'level': 1 },
        { 'symbol': 'LTC/USD', 'level': 1 }
    ]}))

    thread.start_new_thread(run, ())

def print_json(parsed_json):
    print(json.dumps(parsed_json, indent=4))


if __name__ == "__main__":

    # /GET currencies
    r = requests.get(url = 'https://'+config.api_host+'/api/v1/currencies',  headers=headers ) 
    data = r.json()
    print_json(data)

    # /GET symbols
    r = requests.get(url = 'https://'+config.api_host+'/api/v1/currencies',  headers=headers ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    # /GET accounts
    r = requests.get(url = 'https://'+config.api_host+'/api/v1/accounts',  headers=headers ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    # /GET orders
    r = requests.get(url = 'https://'+config.api_host+'/api/v1/orders',  headers=headers ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    # /GET positions
    r = requests.get(url = 'https://'+config.api_host+'/api/v1/positions',  headers=headers ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    # /GET closed_positions
    r = requests.get(url = 'https://'+config.api_host+'/api/v1/closed_positions',  headers=headers ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    # /POST Limit Entry
    r = requests.post(url = 'https://'+config.api_host+'/api/v1/orders',  headers=headers, data = {
        'account_id': config.api_account,
        'order_type': "LIMIT_ENTRY",
        'symbol': "EUR/USD",
        'side': "BUY",
        'quantity': 10000,
        'price': 1.1280,
        'stop_price': 1.12,
        'limit_price': 1.15,
        'client_order_id': "order-entry_stop-buy-"+config.api_account        
    } ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
        limit_entry_order_id = data['order']['order_id']
    else:
        print('error', r.status_code)

    # /PATCH Limit Entry
    r = requests.patch(url = 'https://'+config.api_host+'/api/v1/orders',  headers=headers, data = {
        'order_id': limit_entry_order_id,
        'price': 1.1281

    } ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)


    # /POST Limit Entry
    r = requests.delete(url = 'https://'+config.api_host+'/api/v1/orders',  headers=headers, data = {
        'order_id': limit_entry_order_id
    } ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)


    # /POST Market order
    r = requests.post(url = 'https://'+config.api_host+'/api/v1/orders',  headers=headers, data = {
        'account_id': config.api_account,
        'order_type': "MARKET",
        'symbol': "EUR/USD",
        'side': "BUY",
        'quantity': 10000,
        'price': 1.1280,
        'client_order_id': "order-market-buy-"+config.api_account        
    } ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
        position_id = data['positions'][0]['position_id']
    else:
        print('error', r.status_code)


    # /POST Market order
    r = requests.post(url = 'https://'+config.api_host+'/api/v1/orders',  headers=headers, data = {
        'account_id': config.api_account,
        'order_type': "MARKET",
        'position_id': position_id,
        'symbol': "EUR/USD",
        'side': "SELL",
        'quantity': 10000,
        'price': 1.1280,
        'client_order_id': "order-market-sell-"+config.api_account        
    } ) 
    if r.status_code == 200:
        data = r.json()
        print_json(data)
    else:
        print('error', r.status_code)

    raise SystemExit

    