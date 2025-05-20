# import numpy as np
# from typing import Optional, List, Union

# from chess.chess_types import PieceType, Vector,
from chess.chess_types import Position
from chess.chess_types import TileType#, Loyalty, Direction, Vector

from chess.tiles.tile import Tile

from chess.asset_loader import asset_loader as al
# from globalref import OBJREF

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
        
        sprite = al.tile_sprites.get(tiletype, None)
        super().__init__(position, tiletype, sprite=sprite)
        
        # if self.sprite is None: self.sprite = al.DEFAULT_TILE_SPRITE
