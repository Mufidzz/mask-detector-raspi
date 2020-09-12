from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import cv2 as cv
import os

def detect_face(frame, faceNet, maskNet):
    (h, w) = frame.shape[:2]
    blob = cv.dnn.blobFromImage(frame, 1.0, (300,300), (104.0, 177.0, 123.0))
    faceNet.setInput(blob)
    detections = faceNet.forward()

    faces = []
    face_locations = []
    mask_predictions = []

    for i in range(0, detections.shape[2]):
        confidence = detections[0,0,i,2]

        if confidence > 0.5:
            bounding_box = detections[0,0,i, 3:7] * np.array([w, h, w, h])
            (sX, sY, eX, eY) = bounding_box.astype("int")
        
            (sX, sY) = (max(0, sX), max(0, sY))
            (eX, eY) = (min(w - 1, eX), min(h - 1, eY))

            face = frame[sY:eY, sX:eX]
            face = cv.cvtColor(face, cv.COLOR_BGR2RGB)
            face = cv.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            faces.append(face)
            face_locations.append((sX, sY, eX, eY))
            
    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        mask_predictions = maskNet.predict(faces, batch_size=32)

    return (face_locations, mask_predictions)


def load_self_model(): 
    prototxtPath = "/home/fidz/Desktop/facemask_v2/models/deploy.prototxt"
    weightsPath = "/home/fidz/Desktop/facemask_v2/models/res10_300x300_ssd_iter_140000.caffemodel"
    faceNet = cv.dnn.readNet(prototxtPath, weightsPath)

    maskNet = load_model("/home/fidz/Desktop/facemask_v2/models/mask_detector.model")
    return (faceNet, maskNet)

def exit_camera(): 
    cam.release()
    cv.destroyAllWindows()

def change_camera_resolution_480p(cam):
    cam.set(3, 640)
    cam.set(4, 480)

# MAIN FUNCTION ==============================================================================




