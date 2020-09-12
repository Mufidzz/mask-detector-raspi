import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class PumpDriver:
    def __init__(self, relay_pin):
        self.__RelayPin = relay_pin
        GPIO.setup(self.__RelayPin, GPIO.OUT)

    def pump(self, duration=9999):
        GPIO.output(self.__RelayPin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.__RelayPin, GPIO.LOW)
    