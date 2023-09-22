from PyQt5.QtWidgets import  QWidget
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QStyle, QMessageBox, QAbstractItemView, QLineEdit, QDialog, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QListWidget, QListWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QDrag, QKeyEvent
from PyQt5.QtCore import QEvent, QObject, Qt, QMimeData, QSize, QByteArray, QIODevice, QDataStream, QTimer
import random
from base import *


from .kanban import *
from .utils import *



##
# QListWidgetItem wrapper.
##
class BoardItem(QWidget):
    def __init__(self, parent, item=None, text=None):
        super().__init__()
        self.parent = parent
        self.item   = item
        self.text   = text
        
        self.setObjectName("#container-left-board-item")

        # dimensions
        self.icon_w = 10
        self.icon_h = 10
        
        self.initUi()
        
    def initUi(self):
        hbox      = QHBoxLayout()
        
        stacked   = QStackedWidget(objectName = "#stacked-left-board-item")
        view_line = self.wgtLabelView(self.text)
        edit_line = self.wgtLineEdit(self.text)
        btn_del   = self.wgtBtnDelete()
        btn_edit  = self.wgtBtnEdit()
        
        stacked.addWidget(view_line)
        stacked.addWidget(edit_line)
        
        hbox.setSpacing(1)
        hbox.setContentsMargins(1, 1, 1, 1)
        
        hbox.addWidget(stacked, 70)
        hbox.addWidget(btn_edit, 15)
        hbox.addWidget(btn_del, 15)
        
        self.setLayout(hbox)
        
        self.stacked   = stacked
        self.edit_line = edit_line
        self.view_line = view_line
    
    def wgtBtnDelete(self):
        btn = QPushButton(objectName="btn-left-board-item-del", flat=True)
        btn.setIcon(getIcon(QStyle.SP_DialogCancelButton))
        btn.setIconSize(QSize(self.icon_w, self.icon_h))
        btn.setToolTip("delete board")
        btn.clicked.connect(self.clickHandlerDel)
        return btn
                    
    def wgtBtnEdit(self):
        btn = QPushButton(objectName="btn-left-board-item-edit", flat=True)
        btn.setIcon(getIcon(QStyle.SP_DialogHelpButton))
        btn.setIconSize(QSize(self.icon_w, self.icon_h))
        btn.setToolTip("edit board name")
        btn.clicked.connect(self.clickHandlerEdit)
        return btn
    
    def wgtLineEdit(self, text):
        edit = QLineEdit(text, objectName="line-edit-left-board-item")
        edit.setAlignment(Qt.AlignCenter)
        return edit

    def wgtLabelView(self, text):
        view =  QLabel(text, objectName="label-left-board-item")
        view.setAlignment(Qt.AlignCenter)
        return view

    def getBoardName(self):
        return self.view_line.text()

    def clickHandlerEdit(self):
        is_name_changed = False
        if self.stacked.currentWidget() == self.view_line:
            text = self.view_line.text()
            self.edit_line.setText(text)
            self.stacked.setCurrentWidget(self.edit_line)
        else:
            text = self.edit_line.text()
            if text == self.getBoardName():
                Log.info("Board name did not change: {}".format(self.getBoardName()))
            else:
                prev_board_name = self.getBoardName()
                new_board_name  = self.edit_line.text()
                BoardsManager.rename(prev_board_name, new_board_name)
                is_name_changed = True
            self.view_line.setText(text)
            self.stacked.setCurrentWidget(self.view_line)
            if is_name_changed:
                ## redraw the Right Side.
                self.parent.clickHandlerBoardItem(self.item)
        Log.info("Edited board name: {}".format(self.getBoardName()))
        
    def clickHandlerDel(self):
        Log.info("Deleting item: {}".format(self.getBoardName()))
        ret = QMessageBox(QMessageBox.Critical, self.getBoardName(), "Delete this board?", QMessageBox.Ok | QMessageBox.Cancel).exec_()
        if ret == QMessageBox.Ok:
            self.parent.board_list.takeItem(self.parent.board_list.row(self.item))
            BoardsManager.remove(self.getBoardName())
            Log.info("Deleted.")
        else:
            Log.info("Not deleted")
    
    

class LeftSide(QWidget):
    def __init__(self, parent=None, env=None, child=None):
        super().__init__()
        self.initUi()
        self.child = child
        
    def initUi(self):
        vbox          = QVBoxLayout()
        main_title    = self.sideBarLabel()
        board_list    = self.boardsList()
        add_board_btn = self.addBoardButton()

        # remove dead margins
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        
        vbox.addWidget(main_title, 5)
        vbox.addWidget(board_list, 75)
        vbox.addWidget(add_board_btn,20)
        
        add_board_btn.clicked.connect(self.clickHandlerBtnAddBoard)
        board_list.itemClicked.connect(self.clickHandlerBoardItem)
        
        self.board_list = board_list 
        
        #
        # restoring the previous state.
        #
        boards = BoardsManager.all()
        Log.info("Restoring Boards: {}".format(boards))
        for board in boards:
            self.addBoardItem(board)
                
        self.setLayout(vbox)
       
    #
    def addBoardItem(self, text):
        """adds boards to boards list.

        Args:
            text (_type_): _description_
        """
        item       = QListWidgetItem()
        board_item = BoardItem(parent=self, item=item, text=text)
        size       = QSize(self.minimumWidth(), 30) ## QLabelEdit takes min size of parent.
        
        item.setSizeHint(size)
        self.board_list.addItem(item)
        self.board_list.setItemWidget(item, board_item)

    #
    def clickHandlerBoardItem(self, item):
        """ whenever a board is clicked, 
        the UI on right_side is rebuilt.
        BoardName and Tasks are sent from here to other part of UI
        
        child: right side of UI.
        """
        board_item = self.board_list.itemWidget(item)
        board_name = board_item.getBoardName()
        Log.info("Board: {} clicked".format(board_name))
        task_jsons = BoardsManager.tasks(board_name)
        tasks = []
        for task_json in task_jsons:
            tasks.append(JsonManager.read(task_json))
        
        Log.info("Task files: {}".format(task_jsons))
        Log.info("Extracted tasks: {}".format(tasks))    
        
        # sending board name and tasks to Right Side.
        # and recreating the Right Side UI.
        #
        self.child.board_name = board_name
        self.child.tasks      = tasks
        self.child.initUi()


        # self.child.save()
        # QMessageBox(QMessageBox.Information, "t", item.text()).exec_()


    def clickHandlerBtnAddBoard(self):
        board_name, result = BoardDialog.getBoardName()
        if result:
            if BoardsManager.add(board_name):
                self.addBoardItem(text=board_name)
            else:
                QMessageBox(QMessageBox.Critical, board_name, "already exists").exec_()
                Log.error("Board: {} already exists".format(board_name))
            


    def sideBarLabel(self):
        label = QLabel("BOARDS", objectName="label-left")
        label.setAlignment(Qt.AlignLeft)
        label.setAlignment(Qt.AlignVCenter)
        return label
    
    def addBoardButton(self):
        btn = QPushButton("+", objectName="btn-left-add-board")
        btn.setContentsMargins(0, 0, 0, 0)
        btn.setToolTip("Add Board")
        return btn
    
    def boardsList(self):
        list_boards = QListWidget(objectName="list-left-boards")
        list_boards.setSpacing(0)
        return list_boards


class BoardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Board")
        self.setGeometry(200, 200, 300, 100)

        self.layout = QVBoxLayout()
        
        self.task_name_input = QLineEdit(self)
        self.layout.addWidget(self.task_name_input)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)
        
        self.setLayout(self.layout)

    @staticmethod
    def getBoardName(initial_text=""):
        dialog = BoardDialog()
        dialog.task_name_input.setText(initial_text)
        result = dialog.exec_()
        task_name = dialog.task_name_input.text()
        return task_name, result == QDialog.Accepted





class RightSide(QWidget):
    def __init__(self, parent=None, env=None):
        super().__init__()
        self.board_name     = None
        self.tasks          = None
        self.kanban_columns = None
        
    def removeUi(self):
        if self.kanban_columns:
            for key, col in self.kanban_columns.items():
                col.col.saveAllPendingTasks()
        clearLayout(self.layout())
    
    def initUi(self):
        self.removeUi()
        
        vbox     = QVBoxLayout()
        titlebar = self.titleBarLabel()
        space    = self.kanbanBoardSpace()
        
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        
        vbox.addWidget(titlebar, 5)
        vbox.addWidget(space, 95)
        
        self.setLayout(vbox)
        
        ## restore state
        self.restoreTasks()
    
    def titleBarLabel(self):
        self.titlebar = QLabel("Board Name", objectName="label-right-title")
        self.titlebar.setAlignment(Qt.AlignCenter)
        return self.titlebar
    
    def kanbanBoardSpace(self):
        columns = ConfigManager.getBoardSpecificColumns(self.board_name)
        Log.info("Columns for board {} :: {}".format(self.board_name, columns))
        
        space   = QWidget()
        hbox    = QHBoxLayout()
        space.setLayout(hbox)
        dict_ = {}
        for column in columns: 
            kanban_column = KanbanColumn(column, parent=self) 
            dict_[column] = kanban_column
            hbox.addWidget(kanban_column, int(100/len(columns)))
        self.kanban_columns = dict_
        return space
    
    def restoreTasks(self):
        self.titlebar.setText(self.board_name)
        if self.tasks is None:
            return 
        # we will see that.
        # malformed tasks may cause issue here/
        sorted_tasks = sorted(self.tasks, key=lambda d: d['row'])
        for task in sorted_tasks:
            col = task["col"]
            row = task["row"]
            text= task["md"]
            name= None
            try: 
                name = task["name"]
            except:
                name = None
            
            try:
                kc  = self.kanban_columns[col]
                kc.kanbanColAdd(text=text, name=name)
            except Exception as e:
                Log.error("Board: {} has some unidentified Columns. Please check the config file.\nError: {}".format(self.board_name, e))

            
        