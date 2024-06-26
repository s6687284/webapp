import streamlit as st
import pandas as pd
import numpy as np


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache_data(ttl='1d', show_spinner='Sto scaricando i dati da Amazon')
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


st.title('Uber pickups in NYC by start2impact')

data = load_data(10000)

st.subheader('Mostro dati grezzi')
if st.checkbox('mostra'):
    st.write(data)


st.subheader('Numero di pickup per ora della giornata')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader('Mappa dei pickups at %s:00' % hour_to_filter)
st.map(filtered_data)