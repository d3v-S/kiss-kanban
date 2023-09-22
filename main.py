from base import *
from gui import *

# globals
ENV        = Env();

## pyinstaller to find styles.qss
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



def setStyleSheet(app):
    style_qss = ConfigManager.getStyleSheet()
    try:
        ## incase the given stylesheet fails, fall to default.
        Log.info("trying stylesheet: {}".format(style_qss))
        with open(style_qss,"r") as fh:
            app.setStyleSheet(fh.read())
    except:
        Log.info("failed. trying def stylesheet: {}".format(resource_path(DEF_STYLES)))
        with open(resource_path(DEF_STYLES),"r") as fh:
            app.setStyleSheet(fh.read())
        


##
# calling 
##
def main():
    app       = QApplication(sys.argv)
    setStyleSheet(app)
    main_window = MainWindow(env=ENV)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()