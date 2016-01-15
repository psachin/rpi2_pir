'''
Sample file to demonstrate usage of modules
'''
from modules import RPi2
from modules import Messaging

# Import necessary secrets from secret.py
from my_secret import (password,
                       ACCOUNT_SID, ACCOUNT_TOKEN,
                       TEST_ACCOUNT_SID, TEST_ACCOUNT_TOKEN,
                       twilio_number, twilio_test_number,
                       my_number)

# Set PIR and LED pin
rpi = RPi2(PIR_PIN=17, LED_PIN=18)

# Blink thrice with delay of 1 second
rpi.blink(count=3, delay=1)

# If Motion is detected, send Email and SMS
if rpi.is_pir_active():
    Messaging.send_email('iclcoolster@gmail.com',
                         'iclcoolster@gmail.com',
                         password,
                         attachment=RPi2.takepic(),
                         body='Something fishy detected.')

    Messaging.send_sms(my_number,
                       twilio_number,
                       ACCOUNT_SID,
                       ACCOUNT_TOKEN)
