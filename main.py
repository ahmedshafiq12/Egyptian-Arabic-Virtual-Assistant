import sys
import os

from models.ChatBot.ArabicChatBot import ArabicChatBot
from recorders.audioRecorder import* 
from videoRecorder import *
from modules.BubblesGui import *
from models.emotion_detection.extractEmotion import *

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *


from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qtpy.QtCore import  *

os.environ["QT_FONT_DPI"] = "96" 

# SET AS GLOBAL VARIABLES
# ///////////////////////////////////////////////////////////////
widgets = None
toggleMic = 0
model_output = ""
chatbot = ArabicChatBot('files/hf.env')
emotion = 'emotion: neutral'


# EMOTION FRQUENCY AND TRANSLATE 
emotions_frquency = {'emotion: neutral': 0,'emotion: angery' : 0, 'emotion: sad': 0, 'emotion: happy': 0}
emotions_to_Arabic = {'emotion: angery': "غضبان", 'emotion: happy': "سعيد", 'emotion: sad': "حزين", 'emotion: neutral': "عادي"}

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        global widgets
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        widgets = self.ui

        # Create a QWidget to hold the chat bubbles
        widgets.record.clicked.connect(self.recordButton)
        widgets.sendText.clicked.connect(self.message_to)

        # Make the ScrollBar always Reached the end when updated
        widgets.listView.verticalScrollBar().rangeChanged.connect(lambda: widgets.listView.
                             verticalScrollBar().setValue(widgets.listView.verticalScrollBar().maximum()))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Create a thread for Video capturing 
        # ///////////////////////////////////////////////////////////////
        self.frame_thread = FrameCaptureThread()
        self.frame_thread.frameCaptured.connect(self.display_frame)

        
        widgets.textEdit_4.setAlignment(Qt.AlignmentFlag.AlignRight)  # Align text from right to left

        widgets.textEdit_4.setPlaceholderText("أقدر أساعدك ازاي ياصديقي؟                                                            "  )

        self.text = ""
        # Creaing a list obejct for the chat Bubbles
        # ///////////////////////////////////////////////////////////////
        list_view = self.ui.listView
        list_view.setItemDelegate(MessageDelegate()) 
        self.model = MessageModel()
        list_view.setModel(self.model)
        layout = QVBoxLayout()
        layout.addWidget(list_view)
        self.show()

        
    def message_to(self):
        text = widgets.textEdit_4.toPlainText()
        if len(text) == 0:
            print("please enter any text")
        else:
            self.model.add_message(0, text)
            widgets.textEdit_4.setText=""
            self.text = text
            threading.Thread(target=self.what).start()
            

    def what(self):
        global model_output
        model_output = chatbot.respond(self.text)
        self.message_from(model_output)

    def message_from(self, text):
        self.model.add_message(1, text)


    def recordButton(self):
            global toggleMic
            global emotions_frquency
            global emotion

            if toggleMic == False:
                emotions_frquency = {'emotion: angery': 0, 'emotion: happy': 0, 'emotion: sad': 0, 'emotion: neutral': 0}

                widgets.record.setStyleSheet(widgets.record.styleSheet()+"background-color:#FF0000;")
                start_audio_recording("1")
                self.start_capture()
                toggleMic = True

            elif toggleMic == True:
                emotion = self.get_most_emotion(emotions_frquency)
                widgets.record.setStyleSheet(widgets.record.styleSheet()+"background-color:#A8A8A8;")
                stop_audio_recording("1")
                toggleMic = False
                print(emotion)

    def display_frame(self, frame):
        pixmap = QPixmap.fromImage(frame)

        # Extract the emption from the Image
        emotion = frame.text()
        emotions_frquency[emotion] += 1
        self.ui.videoPlaceHolder.setPixmap(mask_image(pixmap.scaled( self.ui.videoPlaceHolder.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)))

    def displayImage(self):
        self.frame_thread = FrameCaptureThread()
        self.frame_thread.frameCaptured.connect(self.display_frame)

    def start_capture(self):
        self.frame_thread.start()

    def resizeEvent(self, event):
        UIFunctions.resize_grips(self)
    
    def get_most_emotion(self, emotions):
        max_value = max(emotions, key=emotions.get)
        return max_value

    # def prepare_text_for_chatbot(text,emotion):
    #     prompt = f"""لقد كان يتحدث قائلا {text} و كان يشعر بأنه {emotion}"""
    #     return prompt
    
        
if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    window.start_capture()
    sys.exit(app.exec())
