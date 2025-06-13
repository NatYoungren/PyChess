import os
import pygame as pg


# INITIALIZE BOTS (DEBUG)
from engine.bots.bot import Bot
from engine.bots.random_bot import RandomBot
from engine.bots.aggro_bot import AggroBot
from utils.chess_types import Loyalty
debug_bots = {Loyalty.WHITE_AUTO: AggroBot(Loyalty.WHITE_AUTO),
              Loyalty.BLACK_AUTO: AggroBot(Loyalty.BLACK_AUTO),
              Loyalty.BLACK: AggroBot(Loyalty.BLACK)}

controlled_factions = (Loyalty.WHITE,
                       Loyalty.BLACK,
                       )


from globalref import OBJREF


# INITIALIZE ASSET LOADER
from utils.asset_loader import AssetLoader
asset_loader = AssetLoader()
OBJREF.AL = asset_loader


# INITIALIZE BOARD
from chess.board import Board
# state_file = 'standard.json'
# state_file = 'obstacle.json'
# state_file = 'void.json'
state_file = 'summoners.json'
# state_file = 'zombie.json'
JSON_STATE = os.path.join('_saved_states', state_file)
board = Board(state_json=JSON_STATE,
            #   controlled_factions=controlled_factions
              )
OBJREF.BOARD = board


# INITIALIZE UI INSTANCE
from ui.chess_ui import ChessUI
ui = ChessUI.from_config()
OBJREF.UI = ui
ui.init_regions()


# INITIALIZE INPUT HANDLER
from ui.input_handler import InputHandler
ih = InputHandler()
OBJREF.IH = ih


# INITIALIZE GAME MANAGER
from engine.game_manager import GameManager
gm = GameManager(bots=debug_bots)
OBJREF.GM = gm


gm.run()
