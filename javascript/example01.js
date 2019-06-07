#!/usr/bin/env node

/*
 Copyright (c) 2019, 11B.io authors, all rights reserved.

 Ordering requests examples
*/

const axios = require('axios');
const querystring = require('querystring');

const config = require('./config');

function request_get(path, headers){
  options = {headers};
  return axios.get(config.API_URL + '/api/v1' + path, options)
    .then(response => {
      return {status: response.status, data: response.data};
    })
    .catch(error => {
      console.error(error);
      return {error, data: {}};
    });
}

function request_post(path, headers, body) {
  options = {headers};
  return axios.post(config.API_URL + '/api/v1' + path, querystring.stringify(body), options)
    .then(response => {
      return {status: response.status, data: response.data};
    })
    .catch(error => {
      console.error(error);
      return {error, data: {}};
    });
}

function request_patch(path, headers, body) {
  options = {headers};
  return axios.patch(config.API_URL + '/api/v1' + path, querystring.stringify(body), options)
    .then(response => {
      return {status: response.status, data: response.data};
    })
    .catch(error => {
      console.error(error);
      return {error, data: {}};
    });
}

function request_delete(path, headers, body) {
  options = {
    headers,
    data: querystring.stringify(body),
  };
  return axios.delete(config.API_URL + '/api/v1' + path, options)
    .then(response => {
      return {status: response.status, data: response.data};
    })
    .catch(error => {
      console.error(error);
      return {error, data: {}};
    });
}

async function main() {
  let res = {};
  let body = {};
  const headers = {
    'Authorization': 'Bearer ' + config.API_KEY,
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
  };

  // GET Currencies
  res = await request_get('/currencies', headers);
  console.log('\nGet Currencies:');
  console.dir(res.data);

  // GET Symbols
  res = await request_get('/symbols', headers);
  console.log('\nGet Symbols:');
  console.dir(res.data);

  // GET Symbols
  let res_quotes = await request_get('/quotes?symbols=EUR/USD,USD/JPY', headers);
  console.log('\nGetQuotes:');
  console.dir(res_quotes.data);
  
  // GET Accounts
  res = await request_get('/accounts', headers);
  console.log('\nGet Accounts:');
  console.dir(res.data);

  // GET Active Orders
  res = await request_get('/orders', headers);
  console.log('\nGet Active Orders:');
  console.dir(res.data);

  // GET Positions
  res = await request_get('/positions', headers);
  console.log('\nGet Positions:');
  console.dir(res.data);

  // GET Closed Positions
  res = await request_get('/closed_positions', headers);
  console.log('\nGet Closed Positions:');
  console.dir(res.data);
  console.log(res_quotes.data.quote_snapshot[0].offer)
  // Create Limit
  body = {
    account_id: config.API_ACCOUNT,
    order_type: 'LIMIT',
    symbol: 'EUR/USD',
    side: 'BUY',
    quantity: 10000,
    price: res_quotes.data.quote_snapshot[0].offer-.0050,
    stop_loss_price: res_quotes.data.quote_snapshot[0].offer-.010,
    take_profit_price: res_quotes.data.quote_snapshot[0].offer,
    client_order_id: 'order-limit-buy-' + config.API_ACCOUNT,
  };
  res = await request_post('/orders', headers, body);
  console.log('\nCreate Limit:');
  console.dir(res.data);
  const limit_order_id = res.data.order.order_id;
  const take_profit_order_id = res.data.linked_orders[0].order_id;

  // Change Entry Price
  body = {
    order_id: limit_order_id,
    price: res_quotes.data.quote_snapshot[0].offer-.0040,
  };
  res = await request_patch('/orders', headers, body);
  console.log('\nChange Limit Price:');
  console.dir(res.data);

  // Delete Limit
  body = {
    order_id: take_profit_order_id,
  };
  res = await request_delete('/orders', headers, body);
  console.log('\nDelete TP:');
  console.dir(res.data);

  // Delete Entry
  body = {
    order_id: limit_order_id,
  };
  res = await request_delete('/orders', headers, body);
  console.log('\nDelete Limit:');
  console.dir(res.data);

  // Create Market Order
  body = {
    account_id: config.API_ACCOUNT,
    order_type: 'MARKET',
    symbol: 'EUR/USD',
    side: 'BUY',
    quantity: 10000,
    price: 1.1218,
    client_order_id: 'order-market-buy-' + config.API_ACCOUNT,
  };
  res = await request_post('/orders', headers, body);
  console.log('\nCreate Market Order:');
  console.dir(res.data);
  const position_id = res.data.positions[0].position_id;

  // Create Closing Market Order
  body = {
    account_id: config.API_ACCOUNT,
    position_id: position_id,
    order_type: 'MARKET',
    symbol: 'EUR/USD',
    side: 'SELL',
    quantity: 10000,
    price: 1.1218,
    client_order_id: 'order-market-buy-' + config.API_ACCOUNT,
  };
  res = await request_post('/orders', headers, body);
  console.log('\nCreate Closing Market Order:');
  console.dir(res.data);
};

main()
  .then(data => {
    process.exit(0);
  })
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
