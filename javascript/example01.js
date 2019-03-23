#!/usr/bin/env node 
/*
 Copyright (c) 2019, 11B.io authors, all rights reserved.
 
 Ordering requests examples

*/
const axios = require("axios");
var querystring = require('querystring');
var config = require('./config')

var headers = { 
    'Authorization': 'Bearer ' + config.API_KEY,   
    'Accept': 'application/json',
    'Content-Type':  'application/x-www-form-urlencoded',
    }

async function request_get(path){
    try {
        const response = await axios.get(config.API_URL+'/api/v1' + path, {headers: headers});
        return {status: response.status, data: response.data};
    } catch (error) {
        return {status: response.status, data: {}, error: error};
    }
}

async function request_post(path, body) {
    try {
        const response = await axios.post(config.API_URL+'/api/v1' + path, querystring.stringify(body), {headers: headers});
        return {status: response.status, data: response.data};
    } catch (error) {
        console.log(error);
        return {status: 0, data: {}, error: error};
    }
}

async function request_patch(path, body) {
    try {
        const response = await axios.patch(config.API_URL+'/api/v1' + path, querystring.stringify(body), {headers: headers});
        return {status: response.status, data: response.data};
    } catch (error) {
        return {status: response.status, data: {}, error: error};
    }
}

async function request_delete(path, body) {
    try {
        const response = await axios.delete(config.API_URL+'/api/v1' + path,  {data: querystring.stringify(body), headers: headers});
        return {status: response.status, data: response.data};
    } catch (error) {
        return {status: response.status, data: {}, error: error};
    }
}

(async function main(){
    let r = {}

    // Currencies
    r = await request_get('/currencies');
    console.dir(r.data);

    // Symbols
    r = await request_get('/symbols');
    console.dir(r.data);
    
    // Accounts
    r = await request_get('/accounts');
    console.dir(r.data);

    // Active orders
    r = await request_get('/orders');
    console.dir(r.data);

    // Positions
    r = await request_get('/positions');
    console.dir(r.data);

    // Closed Positions
    r = await request_get('/closed_positions');
    console.dir(r.data);

    // Create Limit Entry
    r = await request_post('/orders', {
        'account_id': config.API_ACCOUNT,
        'order_type': 'LIMIT_ENTRY',
        'symbol': 'EUR/USD',
        'side': 'BUY',
        'quantity': 10000,
        'price': 1.1280,
        'stop_price': 1.12,
        'limit_price': 1.15,
        'client_order_id': "order-entry_stop-buy-"+config.API_ACCOUNT ,      
    });
    console.dir(r.data);
    let limit_entry_order_id = r.data.order.order_id;
    let limit_order_id = r.data.linked_orders[0].order_id;

    // Change Entry price
    r = await request_patch('/orders', {
        'order_id': limit_entry_order_id,
        'price': 1.1281
    });
    console.dir(r.data);

    // Delete Limit
    r = await request_delete('/orders', {
        'order_id': limit_order_id
    });
    console.dir(r.data);

    // Delete Entry
    r = await request_delete('/orders', {
        'order_id': limit_entry_order_id
    });
    console.dir(r.data);

    // Create Market Order
    r = await request_post('/orders', {
        'account_id': config.API_ACCOUNT,
        'order_type': 'MARKET',
        'symbol': 'EUR/USD',
        'side': 'BUY',
        'quantity': 10000,
        'price': 1.1280,
        'client_order_id': "order-market-buy-"+config.API_ACCOUNT,      
    });
    console.dir(r.data);
    let position_id = r.data.positions[0].position_id;    

    // Create closing Market order
    r = await request_post('/orders', {
        'account_id': config.API_ACCOUNT,
        'position_id': position_id,
        'order_type': 'MARKET',
        'symbol': 'EUR/USD',
        'side': 'SELL',
        'quantity': 10000,
        'price': 1.1280,
        'client_order_id': "order-market-buy-"+config.API_ACCOUNT,      
    });
    console.dir(r.data);

})();
