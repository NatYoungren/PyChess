import numpy as np

from chess.chess_types import Position, Vector
from chess.chess_types import DirCls as D
from chess.chess_types import Loyalty, Piece

from chess.units.piece import ChessPiece

# TODO: Make enum?
class Queen(ChessPiece):
    def __init__(self, board, loyalty: Loyalty, position):
        # TODO: Sprite
        super().__init__(board=board, loyalty=loyalty, piece_type=Piece.QUEEN, position=position)
    
    
    def options(self):
        v_opts = []
        
        # TODO: Just precompute these vectors and store them?

        for v in D.cardiagonal: # Cardinal & diagonal vectors
            for i in range(1, 8):
                poss_pos = self.position + self.orient_vector(v*i)
                
                t = self.board.get_tile(poss_pos)
                if t is None: continue # OOB tile
                
                p = t.piece
                if p is not None: # Stops at/before first piece
                    if p.loyalty != self.loyalty: # No friendly fire
                        v_opts.append(poss_pos)
                    break
                
                v_opts.append(poss_pos)
        
        return v_opts
        