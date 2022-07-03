# pylint: disable=wildcard-import, C0413
from ChessGame.Headless import Headless_ChessGame
from ChessGame.Gui import Gui_ChessGame
from os.path import join, dirname
import sys

sys.path.append(join(dirname(__file__), "ChessGame"))


if __name__ == "__main__":
    Gui = Gui_ChessGame(Headless_ChessGame())
    Gui.root_window.mainloop()
