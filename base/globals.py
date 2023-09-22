#
# KEYS
#
KEY_DIR_BASE  = "DIR_BASE"
KEY_STYLE_LOC = "FILE_STYLES_QSS"

KEY_BOARD_NAME       = "BOARD_NAME"
KEY_BG_COLOR         = "BGCOLORS"
KEY_TIMEOUT_AUTOSAVE = "TIMEOUT_AUTOSAVE"
KEY_MD_CSS           = "MD_CSS"

#
# DEFAULT
#
DEF_STYLES           = "styles.qss"
DEF_TITLE            = "KISS Kanban"
DEF_COLUMNS          = ["inbox", "todo", "in-progress", "done", "paused"]
DEF_BGCOLOR          = None  ## take from qss.
DEF_TIMEOUT_AUTOSAVE = 3000




#
# DEF markdown sheet:
# 
DEF_MD_SHEET = """
    h1 {
        font-size: 16px;
    }
    
    h2 {
        font-size: 14px;
    }

    h3 {
        font-size: 12px;
    }
    
    h4 {
        font-size: 10px;
    }
    
    p, a, div, body, html {
        font-size: 9px;
    }
    
    h1, h2, h3, h4 {
        font-family: JetBrains Mono;
    }

"""