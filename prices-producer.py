from kafka import KafkaProducer
from typing import List 
import json
from datetime import datetime 
from alpaca_config.keys import config 
from alpaca.data import StockHistoricalDataClient, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
def get_producer(brokers: List[str]):
    producer = KafkaProducer(
        bootstrap_servers = brokers,
        key_serializer = str.encode,
        value_serializer = lambda v: json.dumps(v).encode('utf-8') #important step
    )


    return producer

def produce_historical_price(
        redpanda_client: KafkaProducer,
        topic: str,
        start_date: str, 
        end_date: str,
        symbol: List[str]
):
    api =StockHistoricalDataClient(api_key=config['key_id'], secret_key=config['secret_key'])
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    granularity= TimeFrame.Minute
    
    request_params = StockBarsRequest(symbol_or_symbols=symbol, 
                                              timeframe=granularity,
                                              start=start_date,
                                              end=end_date)
    

    price_df = api.get_stock_bars(request_params).df
    price_df.reset_index(inplace=True)

    records = json.loads(price_df.to_json(orient='records'))
    for idx, record in enumerate(records):
        record['provider'] = 'alpaca'

        try:
            future = redpanda_client.send(topic=topic, key=record['symbol'],value=record, timestamp_ms=record['timestamp'])
            _=future.get(timeout=10)
            print(f'record success')
        except Exception as e:
            print(f'error!')
            
if __name__ == '__main__':
    redpanda_client = get_producer(config['redpanda_brokers'])
    produce_historical_price(
    redpanda_client,
        topic='stock-price',
        start_date='2025-03-01',
        end_date= '2025-04-24',
        symbol=['AAPL']
    )

    redpanda_client.close()