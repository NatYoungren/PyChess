# import numpy as np
# from typing import Optional, List, Union

# from chess.chess_types import PieceType, Vector,
from utils.chess_types import Position
from utils.chess_types import TileType#, Loyalty, Direction, Vector

from chess.tiles.tile import Tile

class VoidTile(Tile):
    """
    Void tile subclass.
    """
    
    is_void: bool = True
    # is_blocked: bool = False
    # is_deadly: bool = False # ?
    
    def __init__(self,
                 position: Position,
                 tiletype: TileType = TileType.VOID):
        
        super().__init__(position, tiletype)
        
        # if self.sprite is None: self.sprite = al.DEFAULT_TILE_SPRITE
