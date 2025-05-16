import numpy as np

from chess.chess_types import Position, Vector
from chess.chess_types import DirCls as D
from chess.chess_types import Loyalty, PieceType

from chess.units.piece import ChessPiece

from chess.actions.action import Action
from chess.actions.outcome import Move, Capture, Castle


# TODO: Add some logic for checks and whatnot?
class KingCapture(Action):
    """
    Represents a move/capture action for a king.
    """
    def update(self):
        super().update()
        
        for v in D.cardiagonal: # Cardinal vectors
            for pos, t, p in self.get_line(v, length=1, enemy_ok=True):
                self.outcomes[t] = Move(self.piece, pos) if p is None else Capture(self.piece, pos, p)

class KingCastle(Action):
    """
    Represents a castling action for a king.
    """
    def update(self):
        super().update()
        
        if self.piece.move_count > 0:
            return
        
        for v in D.cardinal: # Cardinal vectors
            # TODO: Allow get_line length to be a 'min-max' tuple!
            for i, (pos, t, p) in enumerate(self.get_line(v, length=4, can_move=False,
                                                          enemy_ok=False, ally_ok=True)):
                if p is None: continue
                if p.piece_type != PieceType.ROOK: continue
                if p.loyalty != self.loyalty: continue
                if p.move_count > 0: continue
                self.outcomes[t] = Castle(self.piece, p)


class King(ChessPiece):
    is_leader: bool = True
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.KING, position=position)
        self.actions.append(KingCapture(self))
        self.actions.append(KingCastle(self))
