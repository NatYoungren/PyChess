import numpy as np
from typing import List, Optional, Self

from chess.chess_types import Position, Vector, Direction
from chess.chess_types import Loyalty, Piece
from chess.chess_types import DirCls as D

from chess.asset_loader import sprite_dict, DEFAULT_SPRITE

class ChessPiece:
    name: str
    piece_type: Piece = Piece.NONE
    loyalty: Loyalty = Loyalty.NONE
    
    sprite: object # TODO: Type
    facing: Direction # +0- X, +0- Y
    
    position: tuple[int, int]
    move_count: int
    
    # TODO: Can I avoid having the pieces store the board?
    #   Global reference instead?
    #   Or pass it in as needed?
    board: object
    
    def __init__(self, board, loyalty: Loyalty=Loyalty.NONE, piece_type: Piece=Piece.NONE, position: Position = (0, 0), sprite=None):
        self.name = self.__class__.__name__

        self.board = board
        self.loyalty: Loyalty = loyalty
        self.piece_type: Piece = piece_type
        
        if sprite is None:
            sprite = sprite_dict.get(self.loyalty, {}).get(self.piece_type, DEFAULT_SPRITE)
        self.sprite = sprite
        
        # TODO: Placeholder, deprecate / improve?
        self.facing = (0, -1) if loyalty == Loyalty.WHITE else (0, 1)
        self.facing = np.asarray(self.facing)
        
        self._position: Position = np.asarray(position) # TODO: Would this be good to store in piece?
        self.move_count: int = 0

        # Should track a turn-stamped history of positions?
        self.position_history: List[Position] = [self.position]
        self.move_history: List[Vector] = []
        # self.capture_history: List[Self] = []
    
    @property
    def position(self) -> Position:
        return np.array(self._position, dtype=int)
    
    @position.setter
    def position(self, value: Position):
        self._position = np.array(value, dtype=int)
    
    def options(self):
        return None
    
    # def facing(self):
    #     return (1, -1)[self.loyalty]
    
    
    # Input vector is relative to facing: [forward/backward, right/left]
    #   [+ is forward, + is right]
    # Output vector is in board coords: [x, y]
    def orient_vector(self, vector: Vector) -> Vector: # TODO: Matrix multiplication solution?
        return vector * self.facing[1] + vector[::-1] * self.facing[0]
    
    def can_move(self):
        pass
    
    def move(self, position: Position):
        curr_tile = self.board[self.position]
        next_tile = self.board[position]
        if next_tile.piece is not None:
            self.capture(next_tile.piece)
        
        curr_tile.piece = None
        next_tile.piece = self
        self.moved_to(position)
    
    def moved_to(self, position: Position):
        vector = position - self.position
        
        self.position = position
        self.position_history.append(position)
        self.move_history.append(vector)
        
        self.move_count += 1

    
    def capture(self, piece: Self):
        # self.capture_history.append(piece)
        piece.captured(self)
    
    def captured(self, piece):
        self.board[self.position].piece = None
        # del self # TODO: What should happen?
    
    def __repr__(self):
        return f'{self.loyalty.name} {self.name}'