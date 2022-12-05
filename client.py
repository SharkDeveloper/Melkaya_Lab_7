#Client
import socket
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

def send_socket():
     try:
          print("Введите данные:")
          email = input(" email = ")
          msg = input(" message = ")
          Socket = bytes(email+"|"+msg,"utf-8")
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
               s.connect((HOST, PORT))
               s.send(Socket)
               data = s.recv(1024)
     except Exception as ex:
          print("Ошибка отправки: ",ex)
          print("Попробуйте еще раз.")
          send_socket()

send_socket()

