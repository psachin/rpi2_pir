import datetime
import RPi.GPIO as GPIO
import time

from picamera import PiCamera


class RPi2:
    def __init__(self, **kwargs):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.PIR = kwargs.get('PIR_PIN')
        self.LED = kwargs.get('LED_PIN')
        if self.PIR: GPIO.setup(self.PIR, GPIO.IN)
        if self.LED: GPIO.setup(self.LED, GPIO.OUT)

    @classmethod
    def takepic(cls, filename=None):
        '''TODO:
        - Nightmode
        - Resolution
        - Framerate
        - Custom annotate text
        '''
        Current_time = datetime.datetime.now()
        time_stamp = current_time.strftime('%Y-%m-%d-%H:%M:%S')

        if filename:
            snap_name = filename
        else:
            snap_name = time_stamp + '.jpg'

        with PiCamera() as camera:
            camera.resolution = (800, 600)
            camera.framerate = 24
            camera.start_preview()
            camera.annotate_text = 'Invasion! @ {}'.format(time_stamp)
            camera.capture(snap_name)
        return {'time_stamp': current_time,
                'file_name': snap_name}

    def blink(self, count=2, delay=0.1):
        if self.LED:
            for i in range(count):
                GPIO.output(self.LED, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(self.LED, GPIO.LOW)
                time.sleep(delay)
        return ValueError('LED_PIN not set')

    def get_pir_status(self):
        if self.PIR:
            return GPIO.input(self.PIR)
        raise ValueError('PIR_PIN not set')
