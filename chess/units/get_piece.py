
from chess.units.piece import ChessPiece

from chess.units.bishop import Bishop
from chess.units.pawn import Pawn
from chess.units.rook import Rook
from chess.units.knight import Knight
from chess.units.queen import Queen
from chess.units.king import King

from chess.chess_types import Loyalty, Piece

# from chess.chess_types import TileType, Position, Vector
# from chess.chess_types import Direction as D


piece_classes = {
    Piece.PAWN: Pawn,
    Piece.BISHOP: Bishop,
    Piece.ROOK: Rook,
    Piece.KNIGHT: Knight,
    Piece.QUEEN: Queen,
    Piece.KING: King,
}

def get_piece_class(piece_type: Piece):
    pc = piece_classes.get(piece_type, None)
    if pc is None:
        print(f"Piece type {piece_type} not found in piece_classes.")
        print(f"Defaulting to ChessPiece.")
        pc = ChessPiece
    return pc