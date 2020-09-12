import RPi.GPIO as GPIO
import time

class DistanceSensor:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    def __init__(self, trig, echo):
        self.__TRIGGER_PIN = trig
        self.__ECHO_PIN = echo

        GPIO.setup(self.__TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.__ECHO_PIN, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.__TRIGGER_PIN, True)
        time.sleep(0.00001)
        GPIO.output(self.__TRIGGER_PIN, False)

        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self.__ECHO_PIN) == 0:
            start_time = time.time()

        while GPIO.input(self.__ECHO_PIN) == 1:
            stop_time = time.time()

        delta_time = stop_time - start_time

        return (delta_time * 34300/2) #DISTANCE
