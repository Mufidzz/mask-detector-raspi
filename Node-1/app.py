import lib.detect_mask.detect as md
from lib.modules.distance.distance_sensor import DistanceSensor
import cv2 as cv

#STATE
person_detected = False;
mask_detected = False;

hand_on_point = False;
normal_temperature = False;

#OTHER 
cam = cv.VideoCapture(0)
md.change_camera_resolution_480p(cam)
faceNet, maskNet = md.load_self_model()

max_q = 20
q = max_q

face_locations = []
mask_predict_results = []

#MODULES
distance_x = DistanceSensor(18, 24)
distance_y = DistanceSensor(4, 17)

while True:
    _, frame = cam.read()
    if q == max_q:
        face_locations, mask_predict_results = md.detect_face(frame, faceNet, maskNet)
        q = 0
    else:
        q = q + 1

    for (face_location, mask_predict_result) in zip(face_locations, mask_predict_results): 
        (startX, startY, endX, endY) = face_location
        (mask, withoutMask) = mask_predict_result

        label = "Mask" if mask > withoutMask else "No Mask" #Q may need not w v

        # Maybe not needed at end

        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)


        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

        cv.putText(frame, label, (startX, startY - 10), cv.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv.rectangle(frame, (startX, startY), (endX, endY), color, 2)


    cv.imshow("Mask Detector", frame)
    cli_key = cv.waitKey(5) & 0xFF
    if cli_key == 27:
        exit_camera()
        break


    # up here 