import numpy as np
from enum import Enum

from utils.chess_types import Position, Vector, Direction
from utils.chess_types import Loyalty, PieceType, TileType


def next_in_enum(enum_val, enum: Enum):
    """
    Return the next piece type.
    """
    r_next = False
    for i, ev in enumerate(enum):
        if r_next:
            return ev
        if enum_val == ev:
            r_next = True
    
    if r_next:
        for ev in enum:
            return ev
    
    