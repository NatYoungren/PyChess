# import numpy as np
# from typing import Optional, List, Union

# from chess.chess_types import PieceType, Vector,
from utils.chess_types import Position
from utils.chess_types import TileType#, Loyalty, Direction, Vector

from chess.tiles.tile import Tile

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
        
        super().__init__(position, tiletype)

    # TODO: Falling/spinning down into the hole animation.
    def update(self):
        super().update()
        if self.piece is not None:
            print(f'ChasmTile: {self.piece} fell to their death in the chasm')
            self.piece = None