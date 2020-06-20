from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)

# log in to the server
username = "soham274@gmail.com"
# input('Enter gmail address: ')  
# x@gmail.com'
password = "pachpande274"
# getpass.getpass('Enter Password: ')
# 'x' Disclaimer: Password is not encrypted
server.ehlo()
server.starttls()
server.ehlo()
server.login(username, password)

fromaddr = username
msg = MIMEMultipart()
msg['From'] = fromaddr


def send_email(subject, body_content, toEmailAddress):
    msg['Subject'] = subject
    msg['To'] = toEmailAddress
    # msg.attach(MIMEText(body_content, 'plain'))
    msg.attach(MIMEText(body_content, 'html'))
    text = msg.as_string()
    # Send mail
    try:
        server.sendmail(fromaddr, toEmailAddress, text)
        return(1)
    # If some error is encountered, print the error details
    except Exception as e:
        print('Error:', e)
        return(e)
