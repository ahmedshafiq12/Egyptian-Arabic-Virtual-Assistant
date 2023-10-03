from Models.ChatBot.ArabicChatBot import ArabicChatBot
from Recorder.VideoRecorder import *
from Models.CVModel.CamScript import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
import cv2


filename = "Default_user"
file_manager(filename)
chatbot = ArabicChatBot('./files/hf.env')


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(875, 758)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet("label.setStyleSheet(\"border :3px solid blue;\"\n"
                                 "                    \"border-top-left-radius :35px;\"\n"
                                 "                    \"border-top-right-radius : 20px; \"\n"
                                 "                    \"border-bottom-left-radius : 50px; \"\n"
                                 "                    \"border-bottom-right-radius : 10px\")")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.WiseMan = QtWidgets.QLabel(self.centralwidget)
        self.WiseMan.setGeometry(QtCore.QRect(220, -20, 351, 81))
        self.WiseMan.setMinimumSize(QtCore.QSize(10, 10))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(36)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.WiseMan.setFont(font)
        self.WiseMan.setAutoFillBackground(True)
        self.WiseMan.setObjectName("WiseMan")
        self.Recording = QtWidgets.QPushButton(self.centralwidget)
        self.Recording.setGeometry(QtCore.QRect(130, 90, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Recording.setFont(font)
        self.Recording.setObjectName("Recording")
        self.Video = QtWidgets.QLabel(self.centralwidget)
        self.Video.setGeometry(QtCore.QRect(170, 180, 511, 341))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(17)
        sizePolicy.setHeightForWidth(self.Video.sizePolicy().hasHeightForWidth())
        self.Video.setSizePolicy(sizePolicy)
        self.Video.setBaseSize(QtCore.QSize(15, 11))
        self.Video.setAutoFillBackground(False)
        self.Video.setStyleSheet("border :5px solid gray;\n"
                                 "border-top-left-radius :20px;\n"
                                 "border-top-right-radius : 20px; \n"
                                 "border-bottom-left-radius : 20px; \n"
                                 "border-bottom-right-radius : 20px")
        self.Video.setMidLineWidth(0)
        self.Video.setText("")
        self.Video.setObjectName("Video")
        self.TextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.TextEdit.setGeometry(QtCore.QRect(10, 570, 371, 131))
        self.TextEdit.setObjectName("TextEdit")
        self.TextnotEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.TextnotEdit.setGeometry(QtCore.QRect(440, 570, 381, 131))
        self.TextnotEdit.setObjectName("TextnotEdit")
        self.Stop = QtWidgets.QPushButton(self.centralwidget)
        self.Stop.setGeometry(QtCore.QRect(410, 90, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Stop.setFont(font)
        self.Stop.setObjectName("Stop")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 875, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.Recording.clicked.connect(self.Start)
        self.Stop.clicked.connect(self.stop)
        self.emotions = {'angery': 0, 'happy': 0, 'sad': 0, 'neutral': 0}

    def display_text(self, text):
        self.TextnotEdit.setPlainText(text)

    def Start(self):
        start_AVrecording(filename)
        cap = cv2.VideoCapture(0)
        while (cap.isOpened()):
            self.emotions = {'angery': 0, 'happy': 0, 'sad': 0, 'neutral': 0}
            ret, frame = cap.read()
            frame, emotion_name = predict_emotion(frame)
            self.emotions[emotion_name] += 1
            self.display(frame, 1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def stop(self):
        max_value = max(self.emotions, key=self.emotions.get)
        stop_AVrecording(filename)
        text = speech2text()
        prompt = f"""لقد كان يتحدث قائلا {text} و كان يشعر بأنه {max_value}"""
        response = chatbot.respond(prompt)
        self.display_text(response)

    def display(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format.Format_RGB888
            else:
                qformat = QImage.Format.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.Video.setPixmap(QPixmap.fromImage(img))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.WiseMan.setText(_translate("MainWindow", "Wise Man"))
        self.Recording.setText(_translate("MainWindow", "Recording"))

        self.Stop.setText(_translate("MainWindow", "Stop"))