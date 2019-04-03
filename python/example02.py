#!/usr/bin/env python3
#
# Copyright (c) 2019, 11B.io authors, all rights reserved.
# 
# Quotes subscription example
#

import json
import requests 
import time
import ssl
import sys
import websocket

try:
    import thread
except ImportError:
    import _thread as thread

from config import config

def on_message(ws, message):
    print('on_mesage', message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print('### closed ###')

def run(*args):
    while True:
        time.sleep(1)

def on_open(ws):
    ws.send(json.dumps({'type': 'subscribe', 'symbols': [
        {'symbol': 'EUR/USD', 'level': 1},
        {'symbol': 'USD/JPY', 'level': 1},
        {'symbol': 'GBP/USD', 'level': 1},
        {'symbol': 'ETH/USD', 'level': 1},
        {'symbol': 'BTC/USD', 'level': 1},
        {'symbol': 'LTC/USD', 'level': 1},
    ]}))

    thread.start_new_thread(run, ())

def main():
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp('wss://' + config.API_URL.split("//")[1]  + '/socket.io/?access_token=Bearer ' + config.API_KEY, \
        on_message = on_message, on_error = on_error, on_close = on_close)
    ws.on_open = on_open

    # websocket lib requires proper ca.pem on your system
    ws.run_forever(sslopt = {'cert_reqs': ssl.CERT_NONE})

    return 0

if __name__ == '__main__':
    sys.exit(main())
