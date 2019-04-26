import smtplib
import config

def send_email(subject, msg, EMAIL_RECIEVER):
    """Email a person with subject and message."""
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(EMAIL_RECIEVER, EMAIL_RECIEVER, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")


subject = "Petition-Pronto"
msg = "Your petition was approved"
EMAIL_RECIEVER ="lussierc@allegheny.edu", "christianll@yahoo.com"

send_email(subject, msg, EMAIL_RECIEVER)
