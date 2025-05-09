import numpy as np
from typing import Dict, Optional, Self

from chess.chess_types import Position, Vector, Direction
from chess.chess_types import Loyalty, Piece
from chess.chess_types import DirCls as D

# from chess.asset_loader import sprite_dict, DEFAULT_SPRITE

# 1. Each action describes a specific SET of move options.
# - "Move" is all moves which cannot capture
# - "Capture" is moves which can capture
#   This would allow each piece to have a constant set of actions.

# One action could have multiple possible outcomes depending on selected tile.

from chess.actions.outcome import Outcome


class Action:
    name: str
    piece: object
    
    # TODO: Tile -> Action?
    #       Union[Tile, Misc?] -> Action
    actions: Dict[Position, Outcome]
    
    def __init__(self, piece):
        self.name = self.__class__.__name__
        self.piece = piece
        # self.action_count = 0
    
    def update(self):
        """
        Update outcomes.
        """
        pass
    
    def realize(self, pos: Position):
        """
        Apply a selected outcome to the board state.
        """
        pass
    
    
    @property
    def position(self) -> Position:
        return self.piece.position
    
    @property
    def loyalty(self) -> Loyalty:
        return self.piece.loyalty
    
    @property
    def piece_type(self) -> Piece:
        return self.piece.piece_type
    
    @property
    def facing(self) -> Direction:
        return self.piece.facing
    
    @property
    def board(self) -> object:
        return self.piece.board
    
    @property
    def move_count(self) -> int:
        return self.piece.move_count
    
    
    