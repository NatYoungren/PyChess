# import numpy as np
# from typing import Optional, List, Union

# from chess.chess_types import PieceType, Vector,
from utils.chess_types import Position
from utils.chess_types import TileType#, Loyalty, Direction, Vector

from chess.tiles.tile import Tile

from utils.asset_loader import asset_loader as al
# from globalref import OBJREF

class WallTile(Tile):
    """
    Wall tile subclass.
    """
    is_blocked: bool = True
    def __init__(self,
                 position: Position,
                 tiletype: TileType = TileType.WALL):
        
        sprite = al.tile_sprites.get(tiletype, (None, None))[int(position[0] % 2 == position[1] % 2)]
        super().__init__(position, tiletype, sprite=sprite)
        
    def update(self):
        super().update()
        if self.piece is not None:
            print(f'WallTile: {self.piece} was crushed by an obstacle.')
            self.piece = None
