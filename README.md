# kiss-kanban
### Keep It Simple Silly - Kanban Board, for single user with minimalistic interface


## What?
A basic minimalistic kanban board, written in PyQt5.


## Why?
I was using Notion as kanban board. Has too many options which I do not use, plus I love monospace fonts, which is not customizable there.
Plus, do not really like web-apps/electron-clones for desktop application.

Wrote a minimal working kanban for tracking my projects


## Requirements:
1. Fonts - JetBrains Mono, Azeret Mono, Fira Sans
2. Pyqt5 and python runtime.


## Some config and basic working:
1. Creates a folder $HOME/Documents/kiss-kanban
2. Looks for a config.json there. (Look at the attached config.json for example)
3. It should open with an empty interface.
4. Click on Add Board (+) to add a board, and click on board to see columns.
5. Columns are configurable per board, check the config.json
6. Colors of columns are configurable, check the config.json
7. Styles.qss included can be overwritten, if it is provided in config.json
8. Default folder can also be changed from config.json
9. All boards create a folder in $HOME/Documents/kiss-kanban/data/{Board-name}
10. Each created task is a .json in the specific board-folder.
11. Each task is auto-saved per 1 second (again configurable) or one some specific triggers.
12. Edit/View buttons lets user to change to edit the task or see the markdown. (double click also works to enter edit mode)
13. Markdown CSS can user-changed, provide the CSS file in config.json


## Bugs:
1. markdown css can not change font-size. IDK why?


## Todo:
1. add keybindings for opening it globally, creating new tasks and others.
2. expose as much customization possible
3. create .deb, .exe and .dmg
4. add proper icons. using help icon for edit (too lazy to add an icon pack)
5. Add Fonts as resources.


## extras:
1. to create .exe using pyinstaller, use: pyinstaller --onefile --windowed --add-data="styles.qss;." main.py
