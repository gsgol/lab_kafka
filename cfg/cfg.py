PRODUCER = 'data_producer'
PRODUCER_CFG = {'bootstrap.servers': 'localhost:9095'}

MODEL_RES = 'model_results'
TRAIN_CFG_CONSUMER = {
    'bootstrap.servers': 'localhost:9095', 'group.id': 'model_training'}
TRAIN_CFG_PRODUCER = {'bootstrap.servers': 'localhost:9095'}

VIZ_CFG = {
    'bootstrap.servers': 'localhost:9095', 'group.id': 'visualizer'}