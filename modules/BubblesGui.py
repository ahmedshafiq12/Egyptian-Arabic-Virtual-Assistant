from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qtpy.QtCore import  *

USER_ME = 0
USER_THEM = 1

BUBBLE_COLORS = {USER_ME: "#0e1118", USER_THEM: "#272731"}
USER_TRANSLATE = {USER_ME: QPoint(20, 0), USER_THEM: QPoint(0, 0)}

BUBBLE_PADDING = QMargins(15, 5, 35, 5)
TEXT_PADDING = QMargins(25, 15, 60, 15)


class MessageDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        painter.save()
        # Retrieve the user,message uple from our model.data method.
        user, text = index.model().data(index, Qt.DisplayRole)

        trans = USER_TRANSLATE[user]
        painter.translate(trans)

        # option.rect contains our item dimensions. We need to pad it a bit
        # to give us space from the edge to draw our shape.
        bubblerect = option.rect.marginsRemoved(BUBBLE_PADDING)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        # draw the bubble, changing color + arrow position depending on who
        # sent the message. the bubble is a rounded rect, with a triangle in
        # the edge.
        painter.setPen(Qt.NoPen)
        color = QColor(BUBBLE_COLORS[user])
        painter.setBrush(color)
        painter.drawRoundedRect(bubblerect, 10, 10)

        # draw the triangle bubble-pointer, starting from the top left/right.
        if user == USER_ME:
            p1 = bubblerect.topRight()
        else:
            p1 = bubblerect.topLeft()
        polygon = QPolygon([p1 + QPoint(-20, 0), p1 + QPoint(20, 0), p1 + QPoint(0, 20)])
        painter.drawPolygon(polygon)

        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        # draw the text
        doc = QTextDocument()
        doc.setTextWidth(textrect.width())
        doc.setDefaultTextOption(toption)
        doc.setDocumentMargin(0)

        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Bold)
        char_format.setForeground(Qt.white)
        font = QFont()
        font.setPointSize(11)  
        font.setBold(True)
        char_format.setFont(font)
        
        cursor = QTextCursor(doc)
        cursor.insertText(text, char_format)

        painter.translate(textrect.topLeft())
        doc.drawContents(painter)
        painter.restore()


    def sizeHint(self, option, index):
        _, text = index.model().data(index, Qt.DisplayRole)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

            

        doc = QTextDocument(text)
        doc.setTextWidth(textrect.width())
        doc.setDefaultTextOption(toption)
        doc.setDocumentMargin(0)

        textrect.setHeight(doc.size().height()+30)
        textrect = textrect.marginsAdded(TEXT_PADDING)
        return textrect.size()



class MessageModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.messages = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Here we pass the delegate the user, message tuple.
            return self.messages[index.row()]

    def rowCount(self, index):
        return len(self.messages)

    def add_message(self, who, text):
        """
        Add an message to our message list, getting the text from the QLineEdit
        """
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.messages.append((who, text))
            # Trigger refresh.
            self.layoutChanged.emit()

