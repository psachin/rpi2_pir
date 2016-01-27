import smtplib
import time

# Mail
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# SMS
from twilio.rest import TwilioRestClient


class Messaging:
    @classmethod
    def send_email(cls, to, frm,
                   from_password,
                   subject='Motion detected!',
                   body=None,
                   attachment=None):
        '''Send email using GMail'''
        # email settings
        toaddr = to
        fromaddr = frm
        msg = MIMEMultipart()
        msg['To'] = toaddr
        msg['From'] = fromaddr
        msg['Subject'] = subject

        if body:
            msg.attach(MIMEText(body, 'plain'))

        if attachment:
            with open(attachment['file_name'], 'rb') as pic:
                attachment = MIMEImage(pic.read())
            msg.attach(attachment)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(fromaddr, from_password)
        server.send_message(msg, fromaddr, toaddr)
        server.quit()

    @classmethod
    def send_sms(cls, to, frm,
                 TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN,
                 message='Motion detected!'):
        '''Send SMS using Twilio client.'''
        client = TwilioRestClient(TWILIO_ACCOUNT_SID,
                                  TWILIO_ACCOUNT_TOKEN)
        message = client.messages.create(
            body = message,
            to = to,
            from_ = frm
        )

    @staticmethod
    def speak(message='Motion detected in this room.'):
        '''TTS: Requires espeak'''
        p = subprocess.Popen(["espeak", "-ven+f3", "-k5", "-s150", message])
