import numpy as np

from chess.chess_types import Position, Vector
from chess.chess_types import DirCls as D
from chess.chess_types import Loyalty, Piece

from chess.units.piece import ChessPiece

# TODO: Make enum?
class Pawn(ChessPiece):
    def __init__(self, board, loyalty: Loyalty, position):
        # TODO: Sprite
        super().__init__(board=board, loyalty=loyalty, piece_type=Piece.PAWN, position=position)
        
    def options(self):
        v_opts = []
        
        m_opts = [] # Move options
        m_opts.append(self.position + self.orient_vector(D.f)) # Single forward
        if self.move_count == 0:
            m_opts.append(self.position + self.orient_vector(D.f * 2)) # Double forward
        
        c_opts = [] # Capture options
        c_opts.append(self.position + self.orient_vector(D.f_l)) # Left diag
        c_opts.append(self.position + self.orient_vector(D.f_r)) # Right diag
        
        # I hate this.
        # Get the tiles instead and observe what is there.
        for poss_pos in m_opts:
            t = self.board.get_tile(poss_pos)
            if t is None: continue
            # TODO: If tile is blocked, continue!
            
            p = t.piece
            if p is not None: continue 
            v_opts.append(poss_pos) # NOTE: Consider flagging the tile itself as an 'option'
            
            
        for poss_pos in c_opts:
            t = self.board.get_tile(poss_pos)
            if t is None: continue # OOB tile
            
            p = t.piece
            if p is None: continue # No piece to capture
            if p.loyalty == self.loyalty: continue # No friendly fire
            
            v_opts.append(poss_pos)
            
        return v_opts
        
    
    def can_move(self):
        pass
