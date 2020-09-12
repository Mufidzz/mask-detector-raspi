import RPi.GPIO as GPIO
import time

class ServoDriver:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    def __init__(self, pwm_pin, init=50, cal = 3):
        self.__PWM_PIN = pwm_pin
        GPIO.setup(self.__PWM_PIN, GPIO.OUT)

        self.__pwm = GPIO.PWM(self.__PWM_PIN, init)
        self.__degree_calibration = cal

    def move(self, deg = 0):
        self.__pwm.ChangeDutyCycle(deg / 18 + self.__degree_calibration)

    