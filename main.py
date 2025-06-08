import os
import pygame as pg



board_csv = 'default_board.csv'
# piece_csv = 'default_pieces.csv'

# board_csv = 'void_board.csv'
# piece_csv = 'void_pieces.csv'

# board_csv = 'obstacle_board.csv'
# piece_csv = 'obstacle_pieces.csv'

piece_csv = 'summoner_pieces.csv'

board_dir = 'chess/board_csvs'
piece_dir = 'chess/piece_csvs'
board_csv_path = os.path.join(board_dir, board_csv)
piece_csv_path = os.path.join(piece_dir, piece_csv)

from globalref import OBJREF

# INITIALIZE BOARD
from chess.board import Board
board = Board(board_csv_path, piece_csv_path)
OBJREF.BOARD = board


# INITIALIZE UI INSTANCE
from ui.chess_ui import ChessUI
ui = ChessUI.from_config()
OBJREF.UI = ui


# INITIALIZE INPUT HANDLER
from ui.input_handler import InputHandler
ih = InputHandler()
OBJREF.IH = ih


# INITIALIZE BOTS (DEBUG)
from engine.bots.bot import Bot
from engine.bots.random_bot import RandomBot
from engine.bots.aggro_bot import AggroBot
from utils.chess_types import Loyalty
debug_bots = {Loyalty.WHITE_AUTO: AggroBot(Loyalty.WHITE_AUTO),
              Loyalty.BLACK_AUTO: AggroBot(Loyalty.BLACK_AUTO),
              Loyalty.BLACK: AggroBot(Loyalty.BLACK)}


# INITIALIZE GAME MANAGER
from engine.game_manager import GameManager
gm = GameManager(bots=debug_bots)
OBJREF.GM = gm


gm.run()
