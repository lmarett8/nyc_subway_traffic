import streamlit as st
import pickle
import pandas as pd

# def load_model():
#   with open('models/author_pipe.pkl', 'rb') as f:
#     the_model = pickle.load(f)
#   return the_model

def calc_fare(num_passengers):
    fare = 2.75
    return round(num_passengers*fare, 2)  

st.title('Subway trip in NY')

df = pd.read_csv('../data/df_cleaned_year.csv')
stations = df.groupby("station")["entries_abs"].sum().sort_values(ascending=False).head(10)
stations = stations.index.tolist()

station_names = ['choose station']
station_names.extend(sorted(stations))
#st.write(station_names)

destination = st.selectbox(label = 'Pick your destination station', options = station_names)
arr_time = st.selectbox(label = 'Pick your time of arrival', options = ['choose time','8am-noon','noon-4pm'])
passengers = st.select_slider(
    'Select number of passengers:',
    options = range(1,11))

# model = load_model()

if st.button('Lets ride!'):
    if destination == 'choose station':
        st.write('Please select your destination')
    else:
        st.write(destination)
        st.write('total fare for', passengers, 'passengers is: $', calc_fare(passengers))
        # probs = model.predict(destination, arr_time)
    #else:
       # st.write('Goodbye')