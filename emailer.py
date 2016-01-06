#!/usr/bin/env python

import datetime

# mail
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from secret import (password,
                    ACCOUNT_SID, ACCOUNT_TOKEN,
                    TEST_ACCOUNT_SID, TEST_ACCOUNT_TOKEN,
                    twilio_number, twilio_test_number,
                    my_number)

# sms
from twilio.rest import TwilioRestClient

# camera
from picamera import PiCamera
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIR = 17
LED = 18
GPIO.setup(PIR, GPIO.IN)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)

SPEAK = False
SMS = False
EMAIL = True

def speak(message='Motion detected in this room.'):
    p = subprocess.Popen(["espeak", "-ven+f3", "-k5", "-s150", message])
    time.sleep(15)

def blink():
    for i in range(3):
        GPIO.output(LED, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(LED, GPIO.LOW)
        time.sleep(0.1)

def takepic():
    current_time = datetime.datetime.now()
    snap_name = current_time.strftime('%Y-%m-%d-%H:%M:%S') + '.jpg'
    with PiCamera() as camera:
        camera.resolution = (800, 600)
        camera.framerate = 24
        camera.start_preview()
        camera.annotate_text = 'Invasion! @ {}'.format(
            current_time.strftime('%Y-%m-%d-%H:%M:%S'))
        camera.capture(snap_name)
    return {'time_stamp': current_time,
            'file_name': snap_name}

def send_email(to, frm='iclcoolster@gmail.com', pic=takepic()):
    # email settings
    toaddr = to
    fromaddr = frm
    msg = MIMEMultipart()
    msg['To'] = toaddr
    msg['From'] = fromaddr
    msg['Subject'] = "[nebio] Motion detected"
    body = "Motion detected at {}".format(
        pic['time_stamp'].strftime('%A, %d %B %Y at %H:%M:%S'))

    with open(pic['file_name'], 'rb') as pic:
        pic = MIMEImage(pic.read())

    msg.attach(pic)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(fromaddr, password)
    server.send_message(msg, fromaddr, toaddr)
    print('Mail sent.')
    server.quit()
    time.sleep(15)

def send_sms(to=my_number, frm=twilio_number, message='Motion detected!'):
    client = TwilioRestClient(ACCOUNT_SID,
                              ACCOUNT_TOKEN)
    message = client.messages.create(
        body = message,
        to = to,
        from_ = frm
    )
    print(message.sid)
    print('SMS sent.')
    time.sleep(15)

while True:
    time.sleep(0.1)
    if GPIO.input(PIR) == 1:
        print('Motion detected!')
        blink()
        if SPEAK == True:
            speak()
        if EMAIL == True:
            send_email('iclcoolster@gmail.com')
        if SMS == True:
            send_sms()
    else:
        print('Waiting')
        time.sleep(0.1)
