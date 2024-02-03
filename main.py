from bs4 import BeautifulSoup
from pathlib import Path
import smtplib,ssl,time,requests



URL = "http://programmer100.pythonanywhere.com/tours/"
ID_EVENT = "displaytimer"
FILE_PATH = Path("data_event.txt")
RECEIVER = "EMAIL WHO WILL RECEIVE"
SENDER = "EMAIL WHO WILL SEND"
PASSWORD = "YOUR GMAIL APP PASSWORD"


def get_html():
    r = requests.get(URL)
    content = r.text
    return content

def get_even(id):
    html_content = get_html()
    soup = BeautifulSoup(html_content,'html.parser')
    event_content = soup.find(id=id)
    return event_content

def email_sending(message,
                  receiver_email=RECEIVER,
                  password=PASSWORD,
                  port_=465,
                  smtp__server='smtp.gmail.com',
                  sender_email=SENDER):

    message_content = f"""Subject : Music Event

    {message}
    """

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp__server,port_,context=context) as server:
        server.login(sender_email,password)
        server.sendmail(sender_email,receiver_email,message_content)
    


def event_storing(event_):
    event = event_
    with open(FILE_PATH,'a') as f:
        f.write(f"{event}\n")

    

def check_exist_event_file(event,file_data):

    if event != "No upcoming tours":
        if FILE_PATH.exists():
            with open(file_data,'r') as file:
                data = file.read()
            if event not in data:
                event_storing(event)
                email_sending(event)

        else:
            event_storing(event)
            email_sending(event)




if __name__ == '__main__':
    while True:
        event_tracker = get_even('displaytimer').get_text()
        print(event_tracker)
        check_exist_event_file(event_tracker,FILE_PATH)
        time.sleep(2)

