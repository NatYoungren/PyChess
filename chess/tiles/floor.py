import numpy as np
from typing import Optional, List, Union

from utils.chess_types import PieceType, Vector, Position
from utils.chess_types import TileType, Loyalty, Direction, Vector

from chess.tiles.tile import Tile

from utils.asset_loader import asset_loader as al
# from globalref import OBJREF

class FloorTile(Tile):
    """
    Floor tile subclass.
    """
    def __init__(self,
                 position: Position,
                 tiletype: TileType = TileType.FLOOR):
        
        sprite = al.tile_sprites.get(tiletype, (None, None))[int(position[0] % 2 == position[1] % 2)]

        super().__init__(position, tiletype, sprite=sprite)
        
        # if self.sprite is None: self.sprite = al.DEFAULT_TILE_SPRITE
