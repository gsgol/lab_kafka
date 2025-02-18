import time
import json
from confluent_kafka import Producer, Consumer
from river import tree, preprocessing, metrics

def train():
    consumer = Consumer({'bootstrap.servers': 'localhost:9095', 'group.id': 'train'})
    consumer.subscribe(['producer'])

    producer = Producer({'bootstrap.servers': 'localhost:9095'})

    model = (
        preprocessing.MinMaxScaler() |
        tree.SGTRegressor()
    )
    mae = metrics.MAE()

    while True:
        message = consumer.poll(1000)
        if message is not None:
            sample = json.loads(message.value().decode('utf-8'))
            y = sample.pop('DepDelayMinutes')
            x = sample
            model.learn_one(x, y)
            mae.update(y, model.predict_one(x))
            producer.produce('model_results', key='1',
                             value=json.dumps({'arrtime': x['ArrTime'], 'mae': mae.get(), 'day_of_month': x['DayofMonth']
                                               }))
            producer.flush()
            time.sleep(2)


if __name__ == "__main__":
    train()
