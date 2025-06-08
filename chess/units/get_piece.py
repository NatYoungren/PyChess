
from chess.units.piece import ChessPiece

# Base chess pieces
from chess.units.bishop import Bishop
from chess.units.pawn import Pawn
from chess.units.rook import Rook
from chess.units.knight import Knight
from chess.units.queen import Queen
from chess.units.king import King

# New chess pieces
from chess.units.summoner import Summoner, Zombie
from chess.units.jester import Jester
from chess.units.sentry import Sentry

from utils.chess_types import Loyalty, PieceType

# from chess.chess_types import TileType, Position, Vector
# from chess.chess_types import Direction as D


piece_classes = {
    PieceType.PAWN: Pawn,
    PieceType.BISHOP: Bishop,
    PieceType.ROOK: Rook,
    PieceType.KNIGHT: Knight,
    PieceType.QUEEN: Queen,
    PieceType.KING: King,
    
    PieceType.SUMMONER: Summoner,
    PieceType.ZOMBIE: Zombie,
    PieceType.JESTER: Jester,
    PieceType.SENTRY: Sentry,
}

def get_piece_class(piece_type: PieceType):
    pc = piece_classes.get(piece_type, None)
    if pc is None:
        print(f"Piece type {piece_type} not found in piece_classes.")
        print(f"Defaulting to ChessPiece.")
        pc = ChessPiece
    return pc