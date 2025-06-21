import numpy as np
from typing import Tuple

from utils.chess_types import Position, Vector
from utils.chess_types import DirCls as D
from utils.chess_types import Loyalty, PieceType

from chess.units.piece import ChessPiece
from chess.actions.action import Action
from chess.actions.outcome import Move, Capture

class PawnMoveOnly(Action):
    """
    Represents a move action for a pawn.
    """
    
    def flag_enpassant(self):
        self.piece.en_passantable = True
        
    def update(self):
        super().update()
        poss_moves = self.get_line(D.f,
                              length=2 if self.move_count == 0 else 1,
                              enemy_ok=False)
        for i, (pos, t, p) in enumerate(poss_moves):
            self.add_outcome(t, Move(self.piece, pos, callback = self.flag_enpassant if i==1 else lambda: None))


class PawnCaptureOnly(Action):
    """
    Represents a capture action for a pawn.
    """
    def update(self):
        super().update()
        for v in (D.f_l, D.f_r):
            for pos, t, p in self.get_line(v,
                                          length=1,
                                          can_move=False):
                self.add_outcome(t, Capture(self.piece, pos, p))
                break


class PawnPassant(Action):
    """
    Represents an en passant capture action for a pawn.
    """
    
    def update(self):
        super().update()
        for hv, dv in ((D.l, D.f_l), (D.r, D.f_r)):
            for pos, t, p in self.get_line(hv,
                                           length=1,
                                           can_move=False):
                if isinstance(p, Pawn) and p.loyalty != self.piece.loyalty and p.en_passantable:
                    for posD, tD, pD in self.get_line(dv, length=1, can_move=True, enemy_ok=False):
                        self.add_outcome(tD, Capture(self.piece, posD, p, l_delta=2))
                        # break
                    
                    


class Pawn(ChessPiece):
    en_passantable: bool
    
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.PAWN, position=position)
        self.en_passantable = False
        self.actions.append(PawnMoveOnly(self))
        self.actions.append(PawnCaptureOnly(self))
        self.actions.append(PawnPassant(self))

    def turn_changed(self):
        if self.board.current_turn == self.loyalty:
            self.en_passantable = False
        super().turn_changed()