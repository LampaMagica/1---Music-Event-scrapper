from bs4 import BeautifulSoup
from pathlib import Path
from io import StringIO
import requests,datetime,time
import streamlit as st
import pandas as pd
import plotly.express as px



URL = 'http://programmer100.pythonanywhere.com/'

def get_value_scrap(url):
    request = requests.get(url)
    html = request.text
    html = BeautifulSoup(html,"html.parser")
    temp_value = html.find(id="temperatureId").text
    return temp_value

# Part II

def get_time():
    value_time_now = datetime.datetime.now()
    value_time_now = value_time_now.strftime("%y-%m-%d-%H-%M-%S")
    return value_time_now

# Part III
def file_check_add(file_name_path,value,time):
    file_name = Path(file_name_path)
    if file_name.exists():
        with open(file_name,'a') as file:
            file.write(f'{time},{value}\n')
    else:
        with open(file_name,'w') as file:
            file.write("date,temperature\n")
            file.write(f'{time},{value}\n')

# def read_file(file_name_path):
#     with open(file_name_path, 'r') as file:
#         return file.read()
    

if __name__ == "__main__":

    
    count = 0
    while True:
        value_scrap = get_value_scrap(URL)
        value_time = get_time()
        file_check_add('data_temp_exercice.txt',value_scrap,value_time)
        st.write(count)
        count += 1
        time.sleep(2)
        if count == 10:
            break

    df = pd.read_csv('data_temp_exercice.txt')
    st.plotly_chart(px.line(x=df['date'],y=df['temperature'], labels={'x':"Date",'y':'Temperature'}))
    