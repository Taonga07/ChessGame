# pylint: disable=wildcard-import, C0413
# fmt: off
from os.path import join, dirname
import sys

sys.path.append(join(dirname(__file__), "ChessGame"))

from ChessGame.Headless import Headless_ChessGame
from ChessGame.Gui import Gui_ChessGame
# fmt: on
if __name__ == "__main__":
    Gui = Gui_ChessGame(Headless_ChessGame())
    Gui.root_window.mainloop()
