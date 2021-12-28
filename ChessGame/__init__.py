#from Headless import Headless_ChessGame
from ChessGame.Pieces import Pawn, Rook, Knight, Bishop, Queen, King
from ChessGame.API import (
    ChessAPI,
    ChessExc,
    InvMoveExc,
    InvColourExc,
    CheckExc,
    CheckMateExc,
    ChessErrs,
)
from ChessGame.Headless import Headless_ChessGame
from ChessGame.Gui import Gui_ChessGame

from ChessGame.sunfish_interface import SunFishModel, board_to_sunfish, sunfish_auto_move
from ChessGame.calculate_move import RandomMove, random_auto_move