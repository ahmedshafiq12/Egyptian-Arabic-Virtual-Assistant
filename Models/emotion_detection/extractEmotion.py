import cv2
import numpy as np
from keras.models import model_from_json
import tensorflow as tf 
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import ImageFont, ImageDraw, Image

emotion_dict  = {
    0: 'angery',
    1: 'happy',
    2: 'sad',
    3: 'neutral'
}
image_dict  = {
    0: 'غضبان',
    1: 'سعيد',
    2: 'حزين',
    3: 'عادي'
}

# load json and create model
json_file = open(r"G:\VGG FER\4 Classes\model.yaml", 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# load weights into new model
emotion_model.load_weights(r"G:\VGG FER\4 Classes\model.h5")
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

            text = image_dict[maxindex]

            fontpath = "arial.ttf" # <== https://www.freefontspro.com/14454/arial.ttf  
            font = ImageFont.truetype(fontpath, 32)

            reshaped_text = arabic_reshaper.reshape(text)
            reordered_text = get_display(reshaped_text)

            img_pil = Image.fromarray(frame)

            draw = ImageDraw.Draw(img_pil)
            
            draw.text((x+5, y-20),reordered_text, font = font)

            frame = np.array(img_pil)

    return frame,emotion_dict[maxindex]




