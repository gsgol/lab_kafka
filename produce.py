import time
import json
import cfg.cfg as cfg
from confluent_kafka import Producer
from river import stream

def produce():
    producer = Producer(cfg.PRODUCER_CFG)

    dateset_size = 300000
    dataset_stream = stream.iter_csv(
        'data/flights.csv',
        converters={
            'Year': int,
            'Month': int,
            'DayofMonth': int,
            'AirTime': float,
            'ArrTime': float,
            'Distance': float,
            'DepDelayMinutes': float
        }
    )

    for i in range(dateset_size):
        X, _ = next(dataset_stream)
        producer.produce(cfg.PRODUCER, key='1',
                         value=json.dumps(X))
        producer.flush()
        print(X)
        time.sleep(2)


if __name__ == "__main__":
    produce()