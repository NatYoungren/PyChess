import numpy as np
from typing import Optional, List, Union

from utils.chess_types import PieceType, Vector, Position
from utils.chess_types import TileType, Loyalty, Direction, Vector

from chess.tiles.tile import Tile

class FloorTile(Tile):
    """
    Floor tile subclass.
    """
    def __init__(self,
                 position: Position,
                 tiletype: TileType = TileType.FLOOR):
        super().__init__(position, tiletype)
        