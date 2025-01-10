import smtplib
from email.message import EmailMessage


def sendmail(fromEmail,toEmail,sub,txt,passwd):
    #load_dotenv()
    #fromEmail = "MS_XUpqJz@trial-z3m5jgrz6zzldpyo.mlsender.net"
    msg = EmailMessage()
    msg.set_content(txt)
    msg['Subject'] = sub
    msg['From'] = fromEmail
    msg['To'] = toEmail
    s = smtplib.SMTP('smtp.mailersend.net', 587)
    s.ehlo()
    # start TLS for security
    s.starttls()
    # Authentication
    s.login(fromEmail, passwd)
    # sending the mail
    s.sendmail(fromEmail, [toEmail], msg.as_string())
    # terminating the session
    print("DONE")
    s.quit()
