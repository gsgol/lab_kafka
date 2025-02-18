import time
import json
import cfg.cfg as cfg
from confluent_kafka import Producer, Consumer
from river import tree, preprocessing, metrics


def x_y_split(x):
    y = x.pop('DepDelayMinutes')
    return x, y


def prepare_data_for_visualizer(x, metric):
    return {'airtime': x['AirTime'], 'distance': x['Distance'],
            'metric': metric, 'day_of_month': x["DayofMonth"]}


def model_training():
    consumer = Consumer(cfg.TRAIN_CFG_CONSUMER)
    consumer.subscribe([cfg.PRODUCER])

    producer = Producer(cfg.TRAIN_CFG_PRODUCER)

    model = (
        preprocessing.StandardScaler() |
        tree.SGTRegressor()
    )
    metric = metrics.MAE()

    while True:
        message = consumer.poll(1000)
        if message is not None:
            sample = json.loads(message.value().decode('utf-8'))
            x, y = x_y_split(sample)
            model.learn_one(x, y)
            metric.update(y, model.predict_one(x))
            to_visualizer = prepare_data_for_visualizer(x, metric.get())
            print(to_visualizer)
            producer.produce(cfg.MODEL_RES, key='1',
                             value=json.dumps(to_visualizer))
            producer.flush()
            time.sleep(2)


if __name__ == "__main__":
    model_training()