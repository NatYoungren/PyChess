import numpy as np
from enum import Enum
from typing import TypeAlias, Tuple



# # #
# Aliases for type hints
Piece: TypeAlias = object # TODO: Deprecate w/ class reference
ChessObject: TypeAlias = object # TODO: Depreceate w/ class reference
Vector: TypeAlias = Tuple[int, int]     # TODO: Use numpy array
Position: TypeAlias = Tuple[int, int]   # TODO: Use numpy array
# # #



# TODO: How to handle promotion? What is a 'promotable' tile.
#       Are promotions consumed?
class TileType(Enum):
    VOID = -1
    DEFAULT = 0
    WALL = 1
    CHASM = 2



# Each piece needs:
#   Loyalty
#   Position
#   Piece type
#   Misc data
class Piece(Enum):
    NONE = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


# class TileState(Enum):
#     EMPTY = 0
#     BLOCKED = 1


class Loyalty(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2




class Direction(Enum): # Make np?
    FORWARD = (0, 1)
    BACKWARD = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    


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
        return np.asarray(Direction.FORWARD.value)
    @classproperty
    def b(cls) -> Vector:
        return np.asarray(Direction.BACKWARD.value)
    @classproperty
    def l(cls) -> Vector:
        return np.asarray(Direction.LEFT.value)
    @classproperty
    def r(cls) -> Vector:
        return np.asarray(Direction.RIGHT.value)
    
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