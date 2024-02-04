from bs4 import BeautifulSoup
from pathlib import Path
import requests, datetime, time, streamlit as st, pandas as pd, plotly.express as px, sqlite3




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
    con = sqlite3.Connection('data-exercice.db')
    cur = con.cursor()
    query = f"INSERT INTO temp_stat VALUES(?,?)"
    count = 0
    while True:
        value_scrap = get_value_scrap(URL)
        value_time = get_time()
        # file_check_add('data_temp_exercice.txt',value_scrap,value_time)
        cur.execute(query,(value_time,value_scrap,))
        con.commit()
        st.write(count)
        count += 1
        time.sleep(2)
        if count == 4:
            break
    all_resultat = cur.execute('SELECT * FROM temp_stat')
    all_resultat = all_resultat.fetchall()
    data_date = [row[0] for row in all_resultat]
    data_temp = [row[1] for row in all_resultat]
    st.plotly_chart(px.line(x=data_date,y=data_temp, labels={'x':"Date",'y':'Temperature'}))
    # df = pd.read_csv('data_temp_exercice.txt')
    # st.plotly_chart(px.line(x=df['date'],y=df['temperature'], labels={'x':"Date",'y':'Temperature'}))
    