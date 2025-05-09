import os
import pygame as pg

from chess.chess_types import Piece, Loyalty

sprite_prefix = os.path.join('assets', 'units')

# TODO: These should probably be in the unit classes.
#       Rework at some point.
# TODO: Make an AssetLoader class?
sprite_dict = {
    Loyalty.WHITE: {
        Piece.PAWN: "W_Pawn.png",
        Piece.KNIGHT: "W_Knight.png",
        Piece.BISHOP: "W_Bishop.png",
        Piece.ROOK: "W_Rook.png",
        Piece.QUEEN: "W_Queen.png",
        Piece.KING: "W_King.png",
        },
    
    Loyalty.BLACK: {
        Piece.PAWN: "B_Pawn.png",
        Piece.KNIGHT: "B_Knight.png",
        Piece.BISHOP: "B_Bishop.png",
        Piece.ROOK: "B_Rook.png",
        Piece.QUEEN: "B_Queen.png",
        Piece.KING: "B_King.png",
    },
    
    # TODO: Find better solution.
    Loyalty.NONE: {
        Piece.NONE: "defaultpiece.png",
    }
}

for loyalty, piece_sprites in sprite_dict.items():
    for piece, sprite_file in piece_sprites.items():
        sprite_dict[loyalty][piece] = pg.image.load(os.path.join(sprite_prefix, sprite_file))

# TODO: Make a 'sprite' getter?
DEFAULT_SPRITE = sprite_dict[Loyalty.NONE][Piece.NONE]