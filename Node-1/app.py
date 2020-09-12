from lib.modules.distance.distance_sensor import DistanceSensor
from lib.modules.pump.pump_driver import PumpDriver
from lib.modules.servo.servo_driver import ServoDriver
from lib.modules.display.lcddriver import LCDDriver

import lib.detect_mask.detect as md
import lib.modules.temperature.temperature_sensor as temperature

import cv2 as cv
import time

#MEMOIZED  
cam = cv.VideoCapture(0)
md.change_camera_resolution_480p(cam)
faceNet, maskNet = md.load_self_model()

max_q = 20
q = max_q

face_locations = []
mask_predict_results = []

#MODULES
distance_top = DistanceSensor(18, 24)
distance_side = DistanceSensor(4, 17)

pump = PumpDriver(5)

servo = ServoDriver(26)

display = LCDDriver()

while True:
    display.lcd_display_string("Stand on Front of me Bitch !!", 1)

    _, frame = cam.read()

    if q == max_q:
        try:
            face_locations, mask_predict_results = md.detect_face(frame, faceNet, maskNet)
            q = 0
        except:
            q = max_q
    else:
        q = q + 1
       
    if len(face_locations) > 0:
        display.lcd_display_string("I Predicting on You Bitch !!", 1)

        for (face_location, mask_predict_result) in zip(face_locations, mask_predict_results): 
            (startX, startY, endX, endY) = face_location
            (mask, withoutMask) = mask_predict_result

            if mask > withoutMask :
                display.lcd_display_string("Get your hand on me !!", 1)
                
                while True:
                    td = distance_top.get_distance() 
                    sd = distance_side.get_distance()
                    
                    display.lcd_display_string("I Predicting your Temperature bitch !!", 1)
                    
                    if td < 10 and sd < 10:
                        object_temp = temperature.get_object_temperature()
                        
                        if object_temp < 37.5:
                            display.lcd_display_string("Lets Get in, you're fucking safe", 1)
                            pump.pump(1)
                            servo.move(90)
                            time.sleep(0.5)
                            servo.move(180)
                            time.sleep(2)
                            servo.move(90)
                            time.sleep(0.5)
                            break
                        else:
                            display.lcd_display_string("Dont touch me with your fucking virus hand, BITCH !!!", 1)
                            time.sleep(5)
                            break

            else :
                display.lcd_display_string("Wear yout Mask Bitch !!", 1)

            # label = "Mask" if mask > withoutMask else "No Mask" #Q may need not w v

            # # Maybe not needed at end
            # color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            # label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            # cv.putText(frame, label, (startX, startY - 10), cv.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            # cv.rectangle(frame, (startX, startY), (endX, endY), color, 2)



    # cv.imshow("Mask Detector", frame)
    cli_key = cv.waitKey(5) & 0xFF
    if cli_key == 27:
        md.exit_camera()
        display.lcd_clear()
        break


    # up here 