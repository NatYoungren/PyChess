import pygame as pg
import numpy as np
from typing import Optional, Union, Tuple, List, Dict

from globalref import GlobalAccessObject

from chess.board import Board
from chess.units.piece import ChessPiece
from chess.tiles.tile import Tile
from chess.actions.outcome import Outcome

from engine.bots.bot import Bot
from engine.bots.random_bot import RandomBot
from engine.bots.aggro_bot import AggroBot

from utils.chess_types import Loyalty, TileType

class GameManager(GlobalAccessObject):
    """
    A class to manage the game state and logic.
    """
    
    auto_turn_timer: int
    auto_tile: Optional[Tile]
    auto_oc: Optional[Outcome]
    FRAME_CLOCK: pg.time.Clock = pg.time.Clock()
    
    bots: Dict[Loyalty, Bot]
    THINKING_FRAMES: int = 15  # Number of frames to wait before showing the outcome
    PREVIEW_FRAMES: int = 15  # Number of frames to show the outcome before executing it
    
    def __init__(self, bots: Optional[Dict[Loyalty, Bot]] = None):
        self.auto_turn_timer: int = -1
        self.auto_tile: Optional[Tile] = None
        self.auto_oc: Optional[Outcome] = None
        
        self.bots = self.init_bots(bots)
        
    
    def run(self):
        """
        Run the game loop.
        """
        self.board.update()
        
        # Main game loop
        while self.ih.running:
            
            # Handle bot turns
            if not self.board.controlled_turn:
                self.run_bot()
            
            # Handle user input
            self.ih.locked_board = not self.board.controlled_turn
            self.ih.update()
            
            self.update()
            # self.ui.update()? # TODO: Seperate assembling and drawing frame?
            self.ui.draw()
            self.wait()
    
    def run_bot(self): # TODO: Improve to use meaningful bots.
        """ Allow bots to make moves. """
        if not self.locked_board:
            # self.auto_tile, self.auto_oc = self.board.random_outcome()
            self.auto_tile, self.auto_oc = self.bots[self.board.current_turn].play() # type: ignore
            
            # Show selected piece + outcomes
            if self.auto_oc is not None:
                self.ui.s_piece = self.auto_oc.piece
                self.ui.h_piece = self.auto_oc.piece
                self.auto_turn_timer = self.THINKING_FRAMES + self.PREVIEW_FRAMES
            else:
                self.auto_turn_timer = 0

        # Show selected outcome after delay
        if self.auto_turn_timer <= self.PREVIEW_FRAMES:
            self.ui.h_tile = self.auto_tile
            
        # Trigger selected outcome
        self.auto_turn_timer -= 1
        if not self.locked_board: # NOTE: Triggers when timer ticks from 1 -> 0
            self.board.realize(self.auto_oc) if self.auto_oc is not None else self.board.next_turn()
            self.ui.s_tile = None


    def init_bots(self, bots: Optional[Dict[Loyalty, Bot]] = None) -> Dict[Loyalty, Bot]:
        """
        Initialize the bots for the game.
        """
        botdict = bots if bots is not None else {}
        for loyalty in self.board.turn_order:
            if loyalty not in botdict:
                # Default to RandomBot if no bot is provided for the loyalty
                botdict[loyalty] = RandomBot(loyalty)
                print(f'No bot provided for {loyalty}, using RandomBot.')
        return botdict
        
    def update(self):
        pass
    
    def wait(self):
        """ Wait for the next frame. """
        self.FRAME_CLOCK.tick(self.ui.fps)
    
    def undo(self):
        """ Undo the last move. """
        pass
    
    def reset(self):
        pass

    @property
    def locked_board(self):
        """
        Return true if the board is locked (e.g., during AI turns).
        """
        return self.auto_turn_timer > 0
    
    # def update(self):
    #     """
    #     Update the game state.
    #     """
    #     if not self.board.controlled_turn:
    #         if self.auto_turn_timer <= 0:
    #             self.auto_tile, self.auto_oc = self.board.random_outcome()
