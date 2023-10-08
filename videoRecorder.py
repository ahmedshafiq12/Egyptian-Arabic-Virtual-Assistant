from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qtpy.QtCore import  *
import cv2
from models.emotion_detection.extractEmotion import *

class FrameCaptureThread(QThread):
    frameCaptured = Signal(QImage)

    def run(self):
        capture = cv2.VideoCapture(0)  # Change 0 to the desired camera index if multiple cameras are available

        while True:
            ret, frame = capture.read()  # Read frame from the camera

            if not ret:
                break

            # Convert frame to RGB format
            frame, emotion = predict_emotion(frame=frame)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create QImage from the frame
            height, width, _ = frame_rgb.shape
            image = QImage(frame_rgb.data, width, height, QImage.Format.Format_RGB888)
            image.setText("emotion",emotion)
            self.frameCaptured.emit(image)  # Emit the captured frame

        capture.release()
    

#Create a circuler Image
def mask_image(image, imgtype ='png', size = 334 ): 

    # Load image 

    # Crop image to a square: 
    imgsize = min(image.width(), image.height()) 
    rect = QRect( 
        (image.width() - imgsize) / 2, 
        (image.height() - imgsize) / 2, 
        imgsize, 
        imgsize, 
        ) 
        
    image = image.copy(rect) 

    # Create the output image with the same dimensions  
    # and an alpha channel and make it completely transparent: 
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32) 
    out_img.fill(Qt.transparent) 

    # Create a texture brush and paint a circle  
    # with the original image onto the output image: 
    brush = QBrush(image) 
    painter = QPainter(out_img) 
    painter.setBrush(brush) 
    painter.setPen(Qt.NoPen) 
    painter.drawEllipse(0, 0, imgsize, imgsize) 
    painter.end() 

    # Convert the image to a pixmap and rescale it.  
    pr = QWindow().devicePixelRatio() 
    pm = QPixmap.fromImage(out_img) 
    pm.setDevicePixelRatio(pr) 
    size *= pr 
    pm = pm.scaled(size, size, Qt.KeepAspectRatio,  
                                Qt.SmoothTransformation) 

    return pm     

    