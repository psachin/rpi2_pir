#!/usr/bin/env python

import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from secret import password

from picamera import PiCamera
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
global file
PIR = 17
GPIO.setup(PIR, GPIO.IN)


def takepic():
    global file
    current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    snap_name = current_time + '.jpg'
    with PiCamera() as camera:
        camera.resolution = (800, 600)
        camera.framerate = 24
        camera.capture(snap_name)
        takepic.file = snap_name


def send_email(to):
    # email settings
    fromaddr = 'iclcoolster@gmail.com'
    toaddr = to

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "RPi test email"

    body = "This is a test mail"

    takepic()
    with open(takepic.file, 'rb') as pic:
        pic = MIMEImage(pic.read())

    msg.attach(pic)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.send_message(msg)
    server.quit()


while True:
    time.sleep(1)
    if GPIO.input(PIR) == 1:
        print('Motion detected, sending mail..')
        send_email('iclcoolster@gmail.com')
        time.sleep(1)
    else:
        print('Waiting for postie')
        time.sleep(0.1)
