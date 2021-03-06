# 11B SPOT API Examples

This repository contains examples of 11B SPOT REST API usage. It was designed to provide instant responses without a need to refresh data after placing order requests or subscribing to websocket. 

In order to use it, you will need to register an account at https://demo.11b.io, save account, url and generate and save api key.

Login to your account, navigate to SYSTEM -> Settings:


![alt text](https://11bio.github.io/examples/api_key_0.png "API KEY 1")


Press "Generate"

![alt text](https://11bio.github.io/examples/api_key_1.png "API KEY 1")


Save these values to safe place, replace dummy values in config.py

```python
class Config():
    API_KEY = '9b680a8b-22d4-4069-b0e6-f6cc97cd9d71'
    API_URL = 'https://api.demo.11b.io'
    API_ACCOUNT = 'A00-000-030'

config = Config()
```

or in config.js

```javascript
module.exports = {
    API_KEY: '9b680a8b-22d4-4069-b0e6-f6cc97cd9d71',
    API_URL: 'https://api.demo.11b.io',
    API_ACCOUNT: 'A00-000-030'
};
  
```

To run Python examples, you'll need [Python 3.6+](https://www.python.org). To run Javascript examples, you need to install [Node.js](https://nodejs.org/).

**Important**: Server is in demo mode and hence will allow only 20 requests per second per IP address. Any excess request will return code 503 (Service Temporarily Unavailable) for now. This is demo protection, [contact us](https://docs.google.com/forms/d/e/1FAIpQLSd60ZSqPlNxEGRJBgShFG9cRyk1px35WdkHqWfGteO1kyypoA/viewform?usp=sf_link) if you'll like to remove that limit off


**Python examples:**

example_01.py - connect and place requests

example_02.py - connect and subscribe to prices


**Javascript examples:**

example_01.js - connect and place requests

example_02.js - connect and subscribe to prices


For more information about requests you can place, visit https://11bio.github.io


After correcting credentials and installing dependencies, you can run examples :

```
pip3 install websocket-client
pip3 install requests

python3 example01.py
python3 example02.py
```

or 

```
npm install

node example01.js
node example02.js
```


Enjoy,
11B.io Team