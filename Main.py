# pylint: disable=wildcard-import
from ChessGame import *

if __name__ == "__main__":
    Gui = Gui_ChessGame(Headless_ChessGame())
    Gui.root_window.mainloop()
