import numpy as np
from typing import Dict, Optional, Self, Callable

from globalref import GlobalAccessObject


from utils.chess_types import Position, Vector, Direction
from utils.chess_types import Loyalty, PieceType
from utils.chess_types import DirCls as D

# from chess.asset_loader import sprite_dict, DEFAULT_SPRITE

# 1. Each action describes a specific SET of move options.
# - "Move" is all moves which cannot capture
# - "Capture" is moves which can capture
#   This would allow each piece to have a constant set of actions.

# One action could have multiple possible outcomes depending on selected tile.

from chess.actions.outcome import Outcome
from chess.tiles.tile import Tile

class Action(GlobalAccessObject):
    name: str
    piece: object
        
    # TODO: Tile -> Action?
    #       Union[Tile, Misc?] -> Action
    
     # TODO: Avoid overwriting with multiple positions!
     #      Use a list?
     #      Or an 'insert' method which handles this?
    outcomes: Dict[Tile, Outcome]
    
    def __init__(self, piece):
        self.name = self.__class__.__name__
        self.piece = piece
        self.outcomes: Dict[Tile, Outcome] = {}
        # self.action_count = 0
    
    def add_outcome(self, tile: Tile, outcome: Outcome) -> bool:
        """
        Add an outcome to the action.
        """
        
        # TODO: Should still 'show' the possible outcome, but not allow it.
        # Skip if cannot afford the leadership cost?
        if self.board.get_leadership(self.piece.loyalty) - outcome.leadership_delta < 0:
            print(f"Action: Not enough leadership to apply outcome {outcome} for tile {tile}.")
            return False
        
        # TODO: Remove this check?
        if tile in self.outcomes:
            print(f"Action: Outcome already exists for tile {tile}.")
            print(f'\tReplacing with {outcome}.')
            print(f'\tPrevious outcome: {self.outcomes[tile]}')
            print(f'\tPiece: {self.piece}')
            # raise ValueError(f"Action: Outcome already exists for tile {tile}.")

        self.outcomes[tile] = outcome
        return True
        
    def update(self):
        """
        Update outcomes.
        """
        self.outcomes.clear()
        
    # # TODO: Would this be useful?
    # def realize(self, pos: Position):
    #     """
    #     Apply a selected outcome to the board state.
    #     """
    #     pass
    
    @property
    def position(self) -> Position:
        return self.piece.position
    
    @property
    def loyalty(self) -> Loyalty:
        return self.piece.loyalty
    
    @property
    def piece_type(self) -> PieceType:
        return self.piece.piece_type
    
    @property
    def facing(self) -> Direction:
        return self.piece.facing
    
    # @property
    # def board(self) -> object:
    #     return self.piece.board
    
    @property
    def move_count(self) -> int:
        return self.piece.move_count
    
    @property
    def orient_vector(self) -> Callable:
        return self.piece.orient_vector
    
    @property
    def at_vec(self) -> Callable:
        return self.piece.at_vec
    
    @property
    def get_line(self) -> Callable:
        return self.piece.get_line