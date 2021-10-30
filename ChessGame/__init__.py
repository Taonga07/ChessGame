# pylint: disable=import-error
from Headless import Headless_ChessGame
from Gui import Gui_ChessGame

if __name__ == "__main__":
    Gui = Gui_ChessGame(Headless_ChessGame())
    Gui.root_window.mainloop()
