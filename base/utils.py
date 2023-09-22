import os
import json 
import glob
from .globals import *
from .log import *
import shutil


class FileManager:
    @staticmethod
    def getPermanentBaseDir():
        """base directory where files are kept: $HOME/Documents/kiss_kanban/.
        Assume it never fails and always creates directory if it does not exists  
        We may need to keep things 

        Returns:
            string: path of the base directory
        """
        home_directory = os.path.expanduser( '~' )
        path           = os.path.join( home_directory, 'Documents', 'kiss_kanban' )
        if not os.path.exists(path):
            os.mkdir(path)
        return path
    
    @staticmethod
    def configFile():
        path        = FileManager.getPermanentBaseDir()
        config_file = os.path.join(path, "config.json")
        if os.path.exists(config_file):
            return config_file
        return None
    
    @staticmethod
    def getBaseDirFromConfigFile():
        config_file = FileManager.configFile()
        if config_file is not None:
            config_dict = JsonManager.read(config_file)
            try:
                return config_dict[KEY_DIR_BASE]
            except:
                return None
        return None
        
    @staticmethod
    def getBaseDir():
        if FileManager.getBaseDirFromConfigFile() is None:
            return FileManager.getPermanentBaseDir()
        else:
            return FileManager.getBaseDirFromConfigFile()
    
    @staticmethod
    def getDataDir():
        """ every task .json is kept in this folder.
        Structure: BASE_DIR/data/ {BOARD_NAME} / {TASK[1,2,3...].json}

        Returns:
            string: path to data directory
        """
        base  = FileManager.getBaseDir()
        data  = os.path.join(base, 'data')
        if not os.path.exists(data):
            os.mkdir(data)
        return data

    
    @staticmethod
    def getBoardDirPath(board_name):
        data      = FileManager.getDataDir()
        board_dir = os.path.join(data, board_name)
        return board_dir
        
    
    @staticmethod
    def getBoardDirIfExists(board_name):
        board_dir = FileManager.getBoardDirPath(board_name=board_name)
        if not os.path.exists(board_dir):
            Log.info("Path: {} does not exists".format(board_dir))
            return None
        return board_dir
    

    @staticmethod
    def createBoardDir(board_name):
        board_dir = FileManager.getBoardDirPath(board_name=board_name)
        if not os.path.exists(board_dir):
            os.mkdir(board_dir)
            return True
        return False
    
    @staticmethod
    def removeBoardDir(board_name):
        board_dir = FileManager.getBoardDirPath(board_name=board_name)
        if os.path.exists(board_dir):
            shutil.rmtree(board_dir)
    
    @staticmethod
    def getAllBoardsDirs():
        data_dir    = FileManager.getDataDir()
        subfolders  = [ f.name for f in os.scandir(data_dir) if f.is_dir() ]
        return subfolders
    
    def renameBoardDir(board_name, new_boardname):
        board_dir     = FileManager.getBoardDirPath(board_name=board_name)
        new_board_dir = FileManager.getBoardDirPath(board_name=new_boardname)
        if FileManager.createBoardDir(new_board_dir):                
                src_dir = board_dir
                dst_dir = new_board_dir
                for p in os.listdir(src_dir):
                    shutil.move(os.path.join(src_dir, p), dst_dir)
                os.rmdir(src_dir)
            #dest = shutil.move(os.path.abspath(board_dir), os.path.abspath(new_boardname), copy_function=shutil.copytree)
        Log.info("Renamed {} -> {}".format(board_dir, new_board_dir))
        # else:
    #         Log.info("Error in renaming.")

    

class JsonManager:
    @staticmethod
    def read(filename):
        f    = open(filename)
        data = json.load(f)
        f.close()
        return data
    
    def write(filename, dict_):
        with open(filename+'.json', 'w') as fp:
            json.dump(dict_, fp) 




##
#
##
class ConfigManager:
    """does everything related to configuration. 
    It reads file EVERYTIME.
    """
    @staticmethod
    def read():
        config_file = FileManager.configFile()
        if config_file is not None:
            config_dict = JsonManager.read(config_file)
            return config_dict
        return None


    @staticmethod
    def getKeysFromConfig(key, default):
        try:
            config_dict = ConfigManager.read()
            return config_dict[key]
        except:
            return default

    @staticmethod
    def getStyleSheet():
        return ConfigManager.getKeysFromConfig(KEY_STYLE_LOC, DEF_STYLES)

    @staticmethod
    def getBoardSpecificColumns(board_name):
        return ConfigManager.getKeysFromConfig(board_name, DEF_COLUMNS)
    
    
    @staticmethod
    def getKanbanColBgColors():
        return ConfigManager.getKeysFromConfig(KEY_BG_COLOR, DEF_BGCOLOR)
    
    @staticmethod
    def getTimeoutAutosave():
        return int(ConfigManager.getKeysFromConfig(KEY_TIMEOUT_AUTOSAVE, DEF_TIMEOUT_AUTOSAVE))
    
    @staticmethod
    def getMdCss():
        fname = ConfigManager.getKeysFromConfig(KEY_MD_CSS, None)
        if fname:
            try:
                with open(fname, "r") as fh:
                    return fh.read()    
            except:
                return DEF_MD_SHEET
        else:
            return DEF_MD_SHEET
                