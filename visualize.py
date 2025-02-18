import json
import streamlit as st
import matplotlib.pyplot as plt
from confluent_kafka import Consumer

def draw_arrtime(arr_time):
    fig, ax = plt.subplots()
    ax.hist(st.session_state['arrtime'], bins=31)
    ax.set_xlabel('Arrival time')
    ax.set_ylabel('count')
    arr_time.pyplot(fig)
    plt.close()

def draw_day_of_month(dof):
    fig, ax = plt.subplots()
    ax.hist(st.session_state['day_of_month'])
    ax.set_xlabel('Day of month')
    ax.set_ylabel('count')
    dof.pyplot(fig)
    plt.close()

def draw_mae(mae):
    mae.line_chart(st.session_state['mae'],
                    x_label='dataset size', y_label='MAE')
    
def start(items):
    for item in items:
        if item not in st.session_state:
            st.session_state[item] = []

def add_values(sample, items):
    for item in items:
        st.session_state[item].append(sample[item])

def visualize():
    items = ['arrtime', 'mae', 'day_of_month']
    start(items)

    consumer = Consumer({'bootstrap.servers': 'localhost:9095', 'group.id': 'visualize'})
    consumer.subscribe(['model_results'])

    arr_time = st.container(border=True)
    arr_time.title('Arrival time distribution')
    arr_time = arr_time.empty()
    dof = st.container(border=True)
    dof.title('Days of month distribution')
    dof = dof.empty()
    mae = st.container(border=True)
    mae.title('MAE')
    mae = mae.empty()

    while True:
        message = consumer.poll(1000)
        if message is not None:
            sample = json.loads(message.value().decode('utf-8'))
            add_values(sample, items)
            draw_arrtime(arr_time)
            draw_day_of_month(dof)
            draw_mae(mae)
            



if __name__ == "__main__":
    visualize()
