import os 
from dotenv import load_dotenv

load_dotenv()

config = {
'key_id': os.getenv('key_id'),
'secret_key': os.getenv('secret_key'), 
'redpanda_brokers': ['localhost:9092'],
'base_url': 'https://data.alpaca.markets/v1beta1/',
'trade_api_base_url':'https://paper-api.alpaca.markets/v2'
}

