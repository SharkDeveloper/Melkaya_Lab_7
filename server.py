import socket
import os
from smtplib import SMTP
from dotenv import load_dotenv
from email.message import EmailMessage
import imaplib
import email
from email.header import decode_header

load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
print(type(HOST),type(PORT))
EMAIL_LOGIN = os.getenv("EMAIL_LOGIN")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ID = 1 #уникальный ID

def create_msg(text):
    global ID
    unique_ID = "00000"+str(ID)
    unique_ID = unique_ID[-5:]
    msg = EmailMessage()
    msg.set_content(text)
    msg['Subject'] = f"[Ticket #{unique_ID}] Mailer"
    ID = ID + 1
    return msg


def smtp_sender(username,text):
    

    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = os.getenv("SMTP_PORT")
    EMAIL_LOGIN = os.getenv("EMAIL_LOGIN") 
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    with SMTP(f"{SMTP_HOST}:{SMTP_PORT}") as smtp:
        smtp.starttls()
        smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        smtp.send_message(create_msg(text),EMAIL_LOGIN,username)
        smtp.send_message(create_msg(text),EMAIL_LOGIN,EMAIL_LOGIN)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.bind((HOST,PORT))
     s.listen(1)
     conn, addr = s.accept()
     with conn:
         print('Connected by', addr)
         while True:
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode("utf-8").split("|")#расшифровка сокета, разбиение почты[0] и сообщения[1]
            if "@" in data[0]:
                smtp_sender(data[0],data[1])
                conn.send(bytes("OK", "UTF-8"))
            else:
                conn.send(bytes("Некорректно введены данные.Попробуйте снова!", "UTF-8"))




