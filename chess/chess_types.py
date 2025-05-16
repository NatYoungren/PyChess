import numpy as np
from enum import Enum
from typing import TypeAlias, Tuple, Dict



# # #
# Aliases for type hints
PieceType: TypeAlias = object # TODO: Deprecate w/ class reference
ChessObject: TypeAlias = object # TODO: Depreceate w/ class reference
Vector: TypeAlias = Tuple[int, int]     # TODO: Use numpy array
Position: TypeAlias = Tuple[int, int]   # TODO: Use numpy array
# # #



# TODO: How to handle promotion? What is a 'promotable' tile.
#       Are promotions consumed?
class TileType(Enum):
    VOID = -1
    DEFAULT = 0
    FLOOR = 1
    WALL = 2
    CHASM = 3



# Each piece needs:
#   Loyalty
#   Position
#   Piece type
#   Misc data
class PieceType(Enum):
    NONE = 0 # TODO: What does this mean now?
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
    
    SUMMONER = 7
    ZOMBIE = 8
    JESTER = 9


# class TileState(Enum):
#     EMPTY = 0
#     BLOCKED = 1


class Loyalty(Enum):
    NONE = 0
    
    WHITE_AUTO = 0.5
    WHITE = 1
    
    BLACK_AUTO = 1.5
    BLACK = 2


class Direction(Enum): # Make np?
    NORTH = (0, 1)
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)

InitFacing: Dict[Loyalty, Direction] = {
    # Loyalty.NONE: (0, 0), # NOTE: SHOULD CREATE ERROR?
    Loyalty.WHITE: (0, -1),
    Loyalty.WHITE_AUTO: (0, -1),
    Loyalty.BLACK: (0, 1),
    Loyalty.BLACK_AUTO: (0, 1),
}


# Utility, allows class properties
class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

# TODO: Replace with simple dirvec (dv) namespace.
#       This seems completely inane after the fact.
class DirCls:
    """
    Utility class for directional 2D numpy vectors.  
    """
    
    @classproperty
    def f(cls) -> Vector:
        return np.asarray(Direction.NORTH.value)
    @classproperty
    def b(cls) -> Vector:
        return np.asarray(Direction.SOUTH.value)
    @classproperty
    def l(cls) -> Vector:
        return np.asarray(Direction.WEST.value)
    @classproperty
    def r(cls) -> Vector:
        return np.asarray(Direction.EAST.value)
    
    @classproperty
    def f_l(cls) -> Vector:
        return cls.f + cls.l
    @classproperty
    def f_r(cls) -> Vector:
        return cls.f + cls.r
    @classproperty
    def b_l(cls) -> Vector:
        return cls.b + cls.l
    @classproperty
    def b_r(cls) -> Vector:
        return cls.b + cls.r
    
    @classproperty
    def cardinal(cls) -> list[Vector]:
        return (cls.f, cls.b, cls.l, cls.r)
    @classproperty
    def diagonal(cls) -> list[Vector]:
        return (cls.f_l, cls.f_r, cls.b_l, cls.b_r)
    
    @classproperty # HAHA rename this though jesus christ
    def cardiagonal(cls) -> list[Vector]:
        return cls.cardinal + cls.diagonal
    
# for dir in Direction:
#     dir.value.flags.writeable = False