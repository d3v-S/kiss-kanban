
from PyQt5 import sip
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QStyle, QApplication


def clearLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                sip.delete(widget)
            else:
                clearLayout(item.layout())
        sip.delete(layout)



def getIcon(icon):
    return QApplication.style().standardIcon(icon)

