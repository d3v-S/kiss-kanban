from .utils import *
from .log import *
import shutil


class Env:
    """ creates environment required for application to work.
    1. Folder structure
    2. Configuration Files
    3. Set up Configuration
    """
    
    def __init__(self):
        pass
    


# class SavedData:
#     """ looks for any saved data in the predefined folders. 
#     If it exists, everytime the application is loaded, saved data will be reloaded.
#     """
#     def __init__(self):
#         pass
    
#     def getBoards(self):
#         """ reads all the board name from data_directory.

#         Returns:
#             _type_: _description_
#         """
#         board_dirs = FileManager.getAllBoardsDirs()
#         Log.info("Boards detected: {}".format(board_dirs))
#         return board_dirs
    
#     def getBoardTasks(self, board_name):
#         """reads all *.json files in board_name directory

#         Args:
#             board_name (_type_): _description_

#         Returns:
#             _type_: _description_
#         """
#         board_dir = FileManager.getBoardDirIfExists(board_name=board_name)
#         if board_name is None:
#             return []        
#         files = glob.glob(board_dir + "/*.json")
#         Log.info("Board Name: {} Tasks: {}".format(board_name, files))
#         return files



class BoardsManager:
    @staticmethod
    def add(board_name):
        return FileManager.createBoardDir(board_name=board_name)
    
    @staticmethod
    def remove(board_name):
        FileManager.removeBoardDir(board_name=board_name)
    
    @staticmethod
    def all():
        return FileManager.getAllBoardsDirs()
    
    @staticmethod
    def tasks(board_name):
        board_dir = FileManager.getBoardDirIfExists(board_name=board_name)
        if board_name is None:
            return []        
        files = glob.glob(board_dir + "/*.json")
        Log.info("Board Name: {} Tasks: {}".format(board_name, files))
        return files
    
    @staticmethod
    def rename(board_name, new_board_name):
        FileManager.renameBoardDir(board_name, new_board_name)

        

