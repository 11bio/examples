var WebSocketClient = require('websocket').client;
var config = require('./config')

const ws = new WebSocketClient();

ws.on('connectFailed', (error) => {
    console.error('Unable to connect WebSocket; Error: ' + error.toString());
    process.exit(1);
});

ws.on('connect', (connection) => {
    

    connection.on('error', (error) => {
        console.error('Unable to connect WebSocket; Error: ' + error.toString());
        process.exit(2);
    });

    connection.on('close', () => {
        ws_connected = false;
        console.log('WebSocket Connection Closed');
        process.exit(3);
    });

    connection.on('message', (message) => {
        if (message.type === 'utf8') {
            console.log('on message', message.utf8Data)
        }
    });

    if (connection.connected) {
        console.log('WebSocket Client Connected');
        ws_connected = true;
        connection.send(JSON.stringify({
            'type': 'subscribe', 'symbols': [
                { 'symbol': 'EUR/USD', 'level': 1 },
                { 'symbol': 'USD/JPY', 'level': 1 },
                { 'symbol': 'GBP/USD', 'level': 1 },
                { 'symbol': 'ETH/USD', 'level': 1 },
                { 'symbol': 'BTC/USD', 'level': 1 },
                { 'symbol': 'LTC/USD', 'level': 1 }
            ]            
        }));

    }
});

ws.connect(
    'wss://'+config.API_URL.split('//')[1]+'/socket.io/?access_token=Bearer ' + config.API_KEY);

