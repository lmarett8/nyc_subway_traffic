import streamlit as st
import pickle
import pandas as pd
import datetime

# Load the model:
def load_model(station_name, col):
    with open(f'../models/{station_name}_{col}_model.pkl', 'rb') as f:
        the_model = pickle.load(f)
    return the_model

# Calculate the fare:
def calc_fare(num_passengers):
    fare = 2.75
    return round(num_passengers*fare, 2)  

# Determine how busy it is at the station:
def get_busy(mean):
    if mean < 5000:
        return "Not busy, safe to travel!"
    elif (mean>= 5000) and (mean<10000):
        return "Moderate passenger traffic, keep distance between yourself and others"
    elif (mean >= 10_000) and (mean < 15000):
        return "Busy, maintain a safe distance between yourself anf others"
    else:
        return "Extremely busy, avoid travelling if possible"    

st.title('Welcome to New York Subway')

# List of the station names in alphabetical order:
station_names = ['34 ST-PENN STA', 'GRD CNTRL-42 ST', '34 ST-HERALD SQ', 'TIMES SQ-42 ST', '42 ST-PORT AUTH', '23 ST', '86 ST', 'FULTON ST', '125 ST', '14 ST-UNON SQ', 'CANAL ST']
station_manes_sorted = ['Choose below']
station_manes_sorted.extend(sorted(station_names))

destination = st.selectbox('Pick your destination station', options = station_manes_sorted)
arr_day = st.date_input("Pick arrival day")

# Nedd to choose a time and put the time in a timeslot since our data comes in a 4-hr time slots
t = st.time_input('Pick arrival time', datetime.time(00, 00))
if (t > datetime.time(00, 00)) and (t <= datetime.time(4,00)):
    arr_time = '04:00:00'
elif (t > datetime.time(4, 00)) and (t <= datetime.time(8,00)):
    arr_time = '08:00:00'
elif (t > datetime.time(8, 00)) and (t <= datetime.time(12,00)):
    arr_time = '12:00:00'
if (t > datetime.time(12, 00)) and (t <= datetime.time(16,00)):
    arr_time = '16:00:00'
elif (t > datetime.time(16, 00)) and (t <= datetime.time(20,00)):
    arr_time = '20:00:00'
else:
    arr_time = '00:00:00'

passengers = st.select_slider('Select number of passengers:', options = range(1,11))

# Create a button and print out the result:
if st.button('Lets ride!'):
    if destination == 'Choose below':
        st.write('Please select your destination')
    else:
        model_entries = load_model(destination, 'entries')
        model_exits = load_model(destination, 'exits')

        arr_datetime = str(arr_day) + " " + arr_time

        preds_entries = model_entries.predict(start = arr_datetime, end = arr_datetime)
        preds_exits = model_exits.predict(start = arr_datetime, end = arr_datetime)
        preds = preds_entries[0]+preds_exits[0]

        st.write('total fare for', passengers, 'passengers is: $', calc_fare(passengers))
        st.write('Expect ', round(preds), ' of passengers at this station')
        st.write(get_busy(preds))