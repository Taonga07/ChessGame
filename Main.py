# pylint: disable=wildcard-import, C0413
from os.path import join
from os import getcwd
import sys 
sys.path.append(join(getcwd(), 'ChessGame'))
from ChessGame import *

if __name__ == "__main__":
    Gui = Gui_ChessGame(Headless_ChessGame())
    Gui.root_window.mainloop()
