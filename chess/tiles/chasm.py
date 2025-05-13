# import numpy as np
# from typing import Optional, List, Union

# from chess.chess_types import PieceType, ChessObject, Vector,
from chess.chess_types import Position
from chess.chess_types import TileType#, Loyalty, Direction, Vector

from chess.tiles.tile import Tile

from chess.asset_loader import asset_loader as al
# from globalref import OBJREF

# TODO: 'Unstable' tiles?
#       Collapse after being stepped on?
#       Or after a certain number of turns?

class ChasmTile(Tile):
    """
    Chasm tile subclass.
    """
    # is_blocked: bool = True
    is_deadly: bool = True

    def __init__(self,
                 position: Position,
                 tiletype: TileType = TileType.CHASM):
        
        sprite = al.tile_sprites.get(tiletype, (None, None))[int(position[0] % 2 == position[1] % 2)]
        super().__init__(position, tiletype, sprite=sprite)

    # TODO: Falling/spinning down into the hole animation.
    def update(self):
        super().update()
        if self.piece is not None:
            print(f'ChasmTile: {self.piece} fell to their death in the chasm')
            self.piece = None