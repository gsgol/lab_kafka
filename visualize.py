import json
import cfg.cfg as cfg
from confluent_kafka import Consumer
import streamlit as st
import matplotlib.pyplot as plt

features = ['airtime', 'distance', 'metric', 'day_of_month']


def create_session():
    for feature in features:
        if feature not in st.session_state:
            st.session_state[feature] = []

def add_values_to_session(sample):
    for feature in features:
        st.session_state[feature].append(sample[feature])


def draw_air_time(air_time):
    fig, ax = plt.subplots()
    ax.hist(st.session_state['day_of_month'], bins=20)
    ax.set_xlabel('Day of month')
    ax.set_ylabel('count')
    air_time.pyplot(fig)
    plt.close()

def draw_corr(corr):
    fig, ax = plt.subplots()
    ax.scatter(st.session_state['airtime'], st.session_state['distance'])
    ax.set_xlabel('Time in air')
    ax.set_ylabel('Distance')
    corr.pyplot(fig)
    plt.close()

def draw_mae(mae):
    mae.line_chart(st.session_state['metric'],
                    x_label='dataset size', y_label='MAE')
    
def visualizer():
    create_session()

    consumer = Consumer(cfg.VIZ_CFG)
    consumer.subscribe([cfg.MODEL_RES])

    air_time = st.container(border=True)
    air_time.title('Days of month distribution')
    air_time = air_time.empty()
    corr = st.container(border=True)
    corr.title('Time in air and distance correlation')
    corr = corr.empty()
    mae = st.container(border=True)
    mae.title('MAE')
    mae = mae.empty()

    while True:
        message = consumer.poll(1000)
        if message is not None:
            sample = json.loads(message.value().decode('utf-8'))
            add_values_to_session(sample)
            draw_air_time(air_time)
            draw_corr(corr)
            draw_mae(mae)
            



if __name__ == "__main__":
    visualizer()