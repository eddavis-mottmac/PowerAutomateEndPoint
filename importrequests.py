import requests
import streamlit as st

url = st.secrets["endpoint"]["url"]

def submitform(data):

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(url, json=data, headers=headers)
    return response


