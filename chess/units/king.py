import numpy as np

from chess.chess_types import Position, Vector
from chess.chess_types import DirCls as D
from chess.chess_types import Loyalty, Piece

from chess.units.piece import ChessPiece

# TODO: Make enum?
class King(ChessPiece):
    def __init__(self, board, loyalty: Loyalty, position):
        # TODO: Sprite
        super().__init__(board=board, loyalty=loyalty, piece_type=Piece.KING, position=position)
    
    
    def options(self):
        v_opts = []
        
        # TODO: Just precompute these vectors and store them?
        
        for v in D.cardiagonal: # Cardinal & diagonal vectors
            poss_pos = self.position + self.orient_vector(v)
            t = self.board.get_tile(poss_pos)
            if t is None: continue # OOB tile
            
            p = t.piece
            if p is not None and p.loyalty == self.loyalty: continue # No friendly fire
            v_opts.append(poss_pos)
    
        return v_opts
        