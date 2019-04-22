import smtplib
import sqlite3

from email.message import EmailMessage


def connectDatabase():
    con = sqlite3.connect(petitiondb.sqlite3)
    return con


with open(con) as fp:
    msg = EmailMessage()
    msg.set_content(fp.read())

    msg['Subject'] = 'The contents of %s' % con
    msg['From'] = me
    msg['To'] = you

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
