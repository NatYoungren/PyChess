import numpy as np
from enum import Enum
from typing import Optional, List, Union

from chess.chess_types import Piece, ChessObject, Vector, Position
from chess.chess_types import TileType, Loyalty, Direction, Vector



# TODO: Validate?
#       Move to board.py?
def board_constructor(tile_array: List[List[TileType]]):
    """
    Constructs a board from a 2D array of TileType.
    """
    height = len(tile_array)
    width = len(tile_array[0])
    
    board = np.zeros((height, width), dtype=object)
    
    for y in range(height):
        for x in range(width):
            tiletype = tile_array[y][x]
            board[y][x] = Tile((x, y), TileType(tiletype)) #  TODO: Implement subclasses and sprites.
    
    return board



class Tile:
    
    def __init__(self,
                 position: Position,
                 tiletype: TileType = TileType.DEFAULT,
                 sprite=None, # TODO: Biome, which decides sprite based on terrain/coords/rng
                 ):
    # def __init__(self, position: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int]):
    
        self.position: Position = position
        self.sprite = sprite
        
        self.tiletype: TileType = tiletype
        # Flags?
        # Triggers?
        
        self.objects: List[ChessObject] = []
        self.piece: Optional[Piece] = None # TODO: Pieces?
    
    # TODO: Implement in subclasses?
    def can_enter(self, piece: Piece):
        return self.tiletype != TileType.WALL and self.tiletype != TileType.VOID
    
    # Custom behavior based on tiletype
    def enter(self, piece: Piece):
        self.piece = piece # TODO: piece.tile = self?

    def leave(self):
        self.piece = None # TODO: piece.tile = None?


    def add_object(self, obj: ChessObject):
        self.objects.append(obj)
    
    def remove_object(self, obj: Union[ChessObject, int, None]=None): # Remove with index?
        if obj is None:
            self.objects = [] # TODO: Delete them?
            
        elif isinstance(obj, int):
            if obj < 0 or obj >= len(self.objects):
                raise IndexError("Object index out of range.")
            self.objects.pop(obj)
            
        else:
            if obj not in self.objects:
                raise ValueError("Object not found in tile.")
            
        self.objects.remove(obj)
    
    def __repr__(self):
        return f"Tile({self.position} : {self.tiletype.name}) -> ({self.piece} : {self.objects})"
    