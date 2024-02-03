import requests
from bs4 import BeautifulSoup


URL = "http://programmer100.pythonanywhere.com/tours/"

def get_html(url):
    r = requests.get(url)
    content = r.text
    return content

def get_even(url,id):
    html_content = get_html(url)
    soup = BeautifulSoup(html_content,'html.parser')
    event_content = soup.find(id=id)
    return event_content


print(get_even(URL,'displaytimer').get_text())
# print(get_html('http://programmer100.pythonanywhere.com/tours/'))