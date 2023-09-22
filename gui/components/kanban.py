from PyQt5.QtWidgets import  QWidget
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QListView, QMessageBox, QStackedWidget, QStackedLayout, QAbstractItemView, QDialog, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QListWidget, QListWidgetItem, QFileDialog
from PyQt5.QtGui import  QPixmap, QImage, QDrag, QKeyEvent, QFont, QFontMetrics, QTextDocument
from PyQt5.QtCore import QSize, QEvent, QObject, Qt, QMimeData, QByteArray, QIODevice, QDataStream, QTimer

import markdown
from base import *
from .utils import *
import random

##
# Kanban Columns
##
class KanbanColumn(QWidget):
    def __init__(self, name, parent=None):
        super().__init__()
        self.name       = name
        self.objectName = "container-kanban-" + self.name
        self.parent     = parent
        self.dir        = FileManager.getBoardDirIfExists(self.parent.board_name)
        
        self.initUi()
    
    def initUi(self):
        tb       = self.titleBar()
        self.col = self.kanbanCol()
        vbox     = QVBoxLayout()
        
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(tb, 5)
        vbox.addWidget(self.col, 95)
        self.setLayout(vbox)        
        
    def titleBar(self):
        titleBar = QLabel(self.name, objectName="label-kanban-col")
        titleBar.setAlignment(Qt.AlignCenter)
        return titleBar

    def kanbanCol(self):
        return DraggableListWidget(objectName="list-kanban-col", name=self.name, parent=self, dir=self.dir)
    
    
    def kanbanColAdd(self, text, name=None, dir=None):
        self.col.addWgtItem(wgt_item=ListItem(parent=self.col), text=text, name=name, dir=dir)
        
            
        
        
##
# The List and ListWidgetItem Custom
##

## ListWidgetToMakeItDraggable
class DraggableListWidget(QListWidget):
    def __init__(self,  name=None, dir=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
       
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setDragEnabled(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDropIndicatorShown(True) 
        self.setAcceptDrops(True)    
        self.setWordWrap(True)
        self.setMovement(QListView.Snap)
        
        self.itemDoubleClicked.connect(self.itemDoubleClickHandler)
        self.name = name
        self.dir  = dir
        self.bgcolor1 = None
        
        bg_colors_map = ConfigManager.getKanbanColBgColors()
        if bg_colors_map is not None:
            try:        
                self.bgcolor1 = bg_colors_map[self.name] 
                self.setStyleSheet("QListWidget {"+"border: 1px solid " + self.bgcolor1 + "; border-left: 0px; border-bottom: 0px;}")
            except:
                pass
        
        
    # add custom widget ListItem as items
    def addWgtItem(self, wgt_item, text=None, row=None, name=None, dir=None):
        item     = QListWidgetItem()
        wgt_item.setParent(self)
        wgt_item.setItem(item)
        if name is not None:
            wgt_item.setName(name)
        else:
            name = random.randint(0, 1000000)
            wgt_item.setName("{}_{}_{}".format(self.name, "task", str(name)))
            
        if text is not None:
            wgt_item.setText(text)
        item.setSizeHint(wgt_item.sizeHint())
        if row is None or row < 0:
            self.addItem(item)
        else:
            self.insertItem(row, item)
        self.setItemWidget(item, wgt_item)
        return wgt_item

    def mousePressEvent(self, event):
        super(DraggableListWidget, self).mousePressEvent(event)
        if not self.indexAt(event.pos()).isValid():
            self.addWgtItem(ListItem(parent=self))
            

    # https://stackoverflow.com/questions/43283252/when-dragging-multiple-items-from-qlistwidget-non-draggable-items-get-removed
    def getSelectedDraggableIndexes(self):
        """ Get a list of indexes for selected items that are drag-enabled. """
        indexes = []
        for index in self.selectedIndexes():
            item = self.itemFromIndex(index)
            if item.flags() & QtCore.Qt.ItemIsDragEnabled:
                indexes.append(index)
        return indexes
 
    ## handle dragging of object
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            super(DraggableListWidget, self).dragEnterEvent(event)
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
            super(DraggableListWidget, self).dragMoveEvent(event)
            
    def dropEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            if not self.indexAt(event.pos()).isValid():
                wgt_item = self.addWgtItem(ListItem(parent=self), text=event.mimeData().text())
            else:
                row = self.row(self.itemAt(event.pos()))
                wgt_item = self.addWgtItem(ListItem(parent=self), text=event.mimeData().text(), row=row)
            wgt_item.toJson()
            
    def startDrag(self, event):
        print("In Start Drag")
        item       = self.currentItem()
        wgt_item   = self.itemWidget(item)
        itemText   = wgt_item.text()
        mimeData   = QMimeData()
        mimeData.setText(itemText)
        
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            if self.currentItem() is not None:
                wi = self.itemWidget(item)
                wi.deleteInfo()
                self.takeItem(self.row(item))


    def itemDoubleClickHandler(self, item):
        wgt_item = self.itemWidget(item)
        wgt_item.clickHandlerBtnEditor()
        
    def itemClickedHandler(self, item):
        print("Single clicked: {}".format(item))
        
        
    def saveAllPendingTasks(self):
        for i in range(0, self.count()):
            item     = self.item(i)
            wgt_item = self.itemWidget(item)
            if wgt_item.text_changed:
                Log.info("Saving Pending Tasks: {}".format(wgt_item.name))
                wgt_item.toJson()
        
## 
# Custom Widget Item:
# - QTextEdit for editin and viewing in column itself
# - button to move it across
# - label to show timestamp of editing
##

class ListItem(QWidget):
    def __init__(self, parent, item=None):
        super().__init__()
        self.parent = parent
        self.item   = item
        self.timer  = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timerTimeoutHandler)
        self.name         = None
        self.accent_color = None
        self.text_changed = False
        if self.parent is not None: 
            self.setObjectName("container-kanban-item-" + self.parent.name)
            self.accent_color = self.parent.bgcolor1
        self.initUi()
        
        
    def setParent(self, parent):
        self.parent = parent
        self.setObjectName("container-kanban-item-" + self.parent.name)
        self.accent_color = self.parent.bgcolor1
        
        
    def setItem(self, item):
        self.item = item
    
    def setName(self, name):
        self.name = name
    
    def initUi(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.mdSetup(), 80)
        vbox.addLayout(self.btnSetup(), 20)

        vbox.setSpacing(2)
        vbox.setContentsMargins(5, 5, 5, 8)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)
        

    def mdSetup(self):
        self.stacked_widget  = QStackedWidget()
        self.markdown_editor = self.mdEditor()
        self.markdown_viewer = self.mdViewer() #QTextEdit(readOnly=True)
        
        self.stacked_widget.addWidget(self.markdown_editor)
        self.stacked_widget.addWidget(self.markdown_viewer)
    
        return self.stacked_widget

    
    def mdEditor(self):
        editor = QTextEdit()
        editor.setObjectName("editor-kanban-item-task")
        editor.setAutoFormatting(QTextEdit.AutoAll)
        editor.setUndoRedoEnabled(True)
        
        font       = editor.currentFont()
        fontmetric = QFontMetrics(font)
        editor.setTabStopWidth(4 * fontmetric.width(' '))
        
        if self.accent_color:
            editor.setStyleSheet("QTextEdit {" + " color: " + self.accent_color +"; }")
        
        
        editor.textChanged.connect(self.textChangedHandler)
        #editor.focusOutEvent.connect(self.clickHandlerBtnEditor)
        
        return editor
    
    
    def mdViewer(self):
        viewer = RichTextEdit(readOnly=True)
        viewer.setObjectName("viewer-kanban-item-task")
        viewer.setDisabled(False)
        
        
        font       = viewer.currentFont()
        fontmetric = QFontMetrics(font)
        viewer.setTabStopWidth(4 * fontmetric.width(' '))
        
        if self.accent_color:
            viewer.setStyleSheet("QTextEdit {" + " color: " + self.accent_color +"; }")
        
        
        return viewer
    
    def text(self):
        return self.markdown_editor.toPlainText()
    
    def setText(self, text):
        self.markdown_editor.setText(text)
        self.clickHandlerBtnEditor() # reset viewer

    
    def deleteButton(self):
        btn_del = QPushButton("delete", objectName="btn-kanban-item-del", flat=True)
        btn_del.clicked.connect(self.clickHandlerBtnDel)
        btn_del.setIcon((getIcon(QStyle.SP_DialogCancelButton)))
        btn_del.setToolTip("delete tasks")
        btn_del.setIconSize(QSize(16, 16))
        
        return btn_del
    
    def openInEditorBtn(self):
        btn_editor = QPushButton("edit/view", objectName="btn-kanban-item-editor", flat=True)
        btn_editor.clicked.connect(self.clickHandlerBtnEditor)
        btn_editor.setIcon(getIcon(QStyle.SP_DialogHelpButton))
        btn_editor.setIconSize(QSize(16, 16))
        btn_editor.setToolTip("edit/save task")
        
        return btn_editor
    
    def btnSetup(self):
        hbox= QHBoxLayout()
        hbox.addWidget(self.deleteButton(), 50)
        hbox.addWidget(self.openInEditorBtn(), 50)
        return hbox
    
    
    def clickHandlerBtnEditor(self):
        if self.stacked_widget.currentWidget() == self.markdown_editor:
            #doc = self.markdown_editor.document()
            
            ## it is done in this way to be able to change the css of 
            ## rendered markdown.
            doc = QTextDocument()
            doc.setDefaultStyleSheet(ConfigManager.getMdCss())
            #doc.setMarkdown(self.markdown_editor.toPlainText())
            html = markdown.markdown(self.markdown_editor.toPlainText())
            #print(html)
            doc.setHtml(html)
            self.markdown_viewer.setDocument(doc)
            self.stacked_widget.setCurrentWidget(self.markdown_viewer)
        else:
            self.stacked_widget.setCurrentWidget(self.markdown_editor)
        
        if self.text_changed:
            self.toJson()
        
    
    def clickHandlerBtnDel(self):
        if self.parent is not None:
            text = self.markdown_editor.toPlainText()
            if len(text) == 0:
                self.deleteInfo()
                self.parent.takeItem(self.parent.row(self.item))
            else:    
                ret = QMessageBox(QMessageBox.Critical, self.name, "Delete this task?", QMessageBox.Ok | QMessageBox.Cancel).exec_()
                if ret == QMessageBox.Ok:
                    self.deleteInfo()
                    self.parent.takeItem(self.parent.row(self.item))
            
    def textChangedHandler(self):
        self.text_changed = True
        if not self.timer.isActive():
            self.timer.start(ConfigManager.getTimeoutAutosave())
        
    def timerTimeoutHandler(self):
        self.toJson()
        
    def toJson(self):
        col  = self.parent.name
        row  = self.parent.row(self.item)
        text = self.markdown_editor.toPlainText()
        json = {
            "name": self.name,
            "col": col,
            "row": row,
            "md" : text
        }
        Log.info("Saving task: {}".format(self.name))
        JsonManager.write(os.path.join(self.parent.dir, self.name), json)
        self.text_changed = False
        return json
    
    
    def deleteInfo(self):
        path     = os.path.join(self.parent.dir, self.name)
        filename = path + ".json"
        try:
            os.remove(filename)
        except:
            print("In some cases, timer triggers of save earlier and the file has been del")
            



class RichTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    def wheelEvent(self, event):
        #https://stackoverflow.com/questions/25813912/enable-text-zoom-via-ctrlwheel-in-qplaintextedit
        super().wheelEvent(event)
    
    
    def viewportEvent(self, event):
        if not self.isReadOnly():
            return super().viewportEvent(event)
        
        if event.type() == event.Leave:
            self.setDisabled(False)
        elif event.type() == event.Enter:
            self.setDisabled(True)
        return super().viewportEvent(event)