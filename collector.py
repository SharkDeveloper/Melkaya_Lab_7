import imaplib
import email
from email.header import decode_header #для дешифровки полученного письма
import os# для чтения переменных окружения
from dotenv import load_dotenv# для чтения переменных окружения
import codecs# для записии кириллицы в файл .log

load_dotenv()


IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_PORT = os.getenv("IMAP_PORT")
EMAIL_LOGIN = os.getenv("EMAIL_LOGIN") 
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
imap.login(EMAIL_LOGIN, EMAIL_PASSWORD)
imap.select("inbox")

res, data = imap.search(None, "ALL")
data = data[0].decode("utf-8").split(" ")[-1]
num_mails = int(data)#узнаю номер последнего письма

res, msg = imap.fetch(str.encode(data), '(RFC822)')
msg = email.message_from_bytes(msg[0][1])
mail_text = msg.get_payload()
subject = msg["Subject"]
subject = decode_header(subject)[0][0]
print(subject,mail_text)

if "[Ticket #" in subject and "] Mailer" in subject:
    with codecs.open("success_request.log","a","utf-8") as file:
        file.write(subject[9:14]+" "+mail_text)
else:
    with codecs.open("error_request.log","a","utf-8") as file:#не читала кириллицу поэтому появился codecs
        file.write(mail_text)