import sys
from .components import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import  QAbstractItemView, QDialog, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QListWidget, QListWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QDrag, QKeyEvent
from PyQt5.QtCore import QEvent, QObject, Qt, QMimeData, QByteArray, QIODevice, QDataStream, QTimer
import random
##
# WidgetFactory
##
class WidgetFactory:
    
    @staticmethod
    def getLeftPartition(env=None, right=None):
        # for some reason, we need to encapsulate leftside() into q Qwidget.
        # else QSS does not work.
        left_side = LeftSide(env=env, child=right)
        left_main = QWidget(objectName="container-left") 
        hbox      = QHBoxLayout()
        
        hbox.setContentsMargins(0, 0, 0, 0) # removes dead space.
        hbox.setSpacing(0)
        
        left_main.setLayout(hbox)
        hbox.addWidget(left_side)
        return left_main, left_side
    
    
    @staticmethod
    def getRightParition(env=None, left=None):
        right_side = RightSide(env=env)
        right_main = QWidget(objectName="container-right")
        hbox       = QHBoxLayout()
        
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        
        right_main.setLayout(hbox)
        hbox.addWidget(right_side)
        return right_main, right_side
    
    @staticmethod
    def getCentralWidgetPartitions(env=None):
        right, right_side = WidgetFactory.getRightParition(env=env) #QWidget()
        left , left_side  = WidgetFactory.getLeftPartition(env=env, right=right_side)   ## deriving class, does not let CSS to apply. IDK reason.
        hbox              = QHBoxLayout()
        
        hbox.addWidget(left, 10)
        hbox.addWidget(right, 90)
        return hbox

##``
# Main Windowd
##
class MainWindow(QMainWindow):
    def __init__(self, env=None) -> None:
        super().__init__()
        self.env = env
        self.initUi()
        self.setWindowTitle(DEF_TITLE)
        
    def initUi(self):
        self.central_widget = QWidget()
        self.layout = WidgetFactory.getCentralWidgetPartitions(env=self.env)
        self.central_widget.setObjectName("#central-widget")
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)