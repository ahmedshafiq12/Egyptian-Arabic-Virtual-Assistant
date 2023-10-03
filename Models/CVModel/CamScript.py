import cv2
import numpy as np
from keras.models import model_from_json
import tensorflow as tf 

emotion_dict  = {
    0: 'angery',
    1: 'happy',
    2: 'sad',
    3: 'neutral'
}

# load json and create model
json_file = open(r"Models/CVModel/model.yaml", 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# load weights into new model
emotion_model.load_weights(r"Models/CVModel/model.h5")
print("Loaded model from disk")



def predict_emotion(frame):
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)
    maxindex = 0 
    # take each face available on the camera and Preprocess it
    if len(num_faces)!= 0:
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
            roi_gray_frame = frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # predict the emotions
            emotion_prediction = emotion_model.predict(cropped_img)
            confidence = np.amax(emotion_prediction)
            print (confidence)
            if(confidence>0.7):
                maxindex = int(np.argmax(emotion_prediction))


            cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    return frame,emotion_dict[maxindex]



