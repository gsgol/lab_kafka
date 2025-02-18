import time
import json
from river import stream
from confluent_kafka import Producer


def produce():
    producer = Producer({'bootstrap.servers': 'localhost:9095'})
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
        producer.produce('producer', key='1',
                         value=json.dumps(X))
        producer.flush()
        time.sleep(2)


if __name__ == "__main__":
    produce()
