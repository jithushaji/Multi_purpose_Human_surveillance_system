import sqlite3
import pandas as pd
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders



def mail(file_name):
    
    SUBJECT = 'Daily Detection Results'
    FILENAME = file_name
    FILEPATH = './attachthisfile.csv'
    MY_EMAIL = 'surveillancesyatem@gmail.com'
    MY_PASSWORD = 'Admin@123'
    TO_EMAIL = 'jithushaji23@gmail.com'
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = COMMASPACE.join([TO_EMAIL])
    msg['Subject'] = SUBJECT
    
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(FILENAME, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=FILENAME)  # or
    # part.add_header('Content-Disposition', 'attachment; filename="attachthisfile.csv"')
    msg.attach(part)
    
    print("sending mail")
    smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(MY_EMAIL, MY_PASSWORD)
    smtpObj.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
    smtpObj.quit()
    print("mail send")
    


def send_Reco():
    conn=sqlite3.connect("survilance.db")
    sql_query = pd.read_sql_query("SELECT * FROM Recognized",conn)
    df = pd.DataFrame(sql_query)
    df.to_csv (r'Recognized.csv', index = False)
    #drop table here
    sql = "DROP TABLE IF EXISTS Recognized"
    cur=conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()
    mail('Recognized.csv')
    
def send_attd():
    conn=sqlite3.connect("survilance.db")
    sql_query = pd.read_sql_query("SELECT * FROM Loggedin",conn)
    df = pd.DataFrame(sql_query)
    df.to_csv (r'Loggedin.csv', index = False)
    #drop table here
    sql = "DROP TABLE IF EXISTS Loggedin"
    cur=conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()
    
    conn.close()
    mail('Loggedin.csv')


    
