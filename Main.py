# pylint: disable=wildcard-import, C0413
from os.path import join, dirname
import sys 
sys.path.append(join(dirname(__file__), 'ChessGame'))
from ChessGame import *

if __name__ == "__main__":
    Gui = Gui_ChessGame(Headless_ChessGame())
    Gui.root_window.mainloop()
