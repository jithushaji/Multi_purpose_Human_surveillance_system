
import smtplib

def send_mail():
    
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security which makes the connection more secure
    smtpobj.starttls()
    senderemail_id="surveillancesyatem@gmail.com"
    senderemail_id_password="Admin@123"
    receiveremail_id="jithushaji23@gmail.com"
    # Authentication for signing to gmail account
    smtpobj.login(senderemail_id, senderemail_id_password)
    # message to be sent
    message = "authorised peron"
    # sending the mail - passing 3 arguments i.e sender address, receiver address and the message
    smtpobj.sendmail(senderemail_id,receiveremail_id, message)
    # Hereby terminate the session
    smtpobj.quit()
    print ("mail send - Using simple text message")
