import numpy as np
from typing import Tuple

from utils.chess_types import Position, Vector
from utils.chess_types import DirCls as D
from utils.chess_types import Loyalty, PieceType

from chess.units.piece import ChessPiece
from chess.actions.action import Action
from chess.actions.outcome import Move, Capture


class SentryJump(Action):
    """
    Represents a move/capture action for a sentry.
    """
    VECTORS: Tuple[Vector] = (D.f+D.f_l, D.f+D.f_r,
                              D.r+D.f_r, D.r+D.b_r,
                              D.b+D.b_l, D.b+D.b_r,
                              D.l+D.f_l, D.l+D.b_l)
    def disable_lurk(self):
        self.piece.is_lurking = False
        self.piece.jump_timer = 2
    
    def update(self):
        super().update()
        if self.piece.jump_timer > 0:
            return
        for v in self.VECTORS: # Knight vectors
            pos, t, p = self.at_vec(v)
            if t is None: continue # OOB tile
            if t.is_blocked: continue # Blocked tile
            if t.is_void: continue # Void tile
            
            if p is None:
                self.outcomes[t] = Move(self.piece, pos, callback=self.disable_lurk)
            elif p.loyalty != self.loyalty: # No friendly fire
                self.outcomes[t] = Capture(self.piece, pos, p, callback=self.disable_lurk)


class SentryAmbush(Action):
    """
    Represents an ambush action for a sentry.
    """
    def disable_lurk(self):
        self.piece.is_lurking = False

    def update(self):
        super().update()
        if not self.piece.is_lurking: return
        for v in (D.f, D.b, D.l, D.r):
            for pos, t, p in self.get_line(v, length=4, can_move=False):
                self.outcomes[t] = Capture(self.piece, pos, p, callback=self.disable_lurk)
        

class SentryLurk(Action):
    """
    Moves nowhere, enables ambush.
    """
    def enable_lurk(self):
        self.piece.is_lurking = True
        
    def update(self):
        super().update()
        if self.piece.is_lurking:
            return
        # TODO: Special color!
        self.outcomes[self.board[self.piece.position]] = Move(self.piece, self.piece.position, callback=self.enable_lurk)


class Sentry(ChessPiece):
    # Sentries cannot jump on consecutive turns
    jump_timer: int = 0 # TODO: This is not indicated visually!
    is_lurking: bool = False # NOTE: Lurking is indicated with sprite change.
    
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.SENTRY, position=position)    
        self.actions.append(SentryJump(self))
        self.actions.append(SentryAmbush(self))
        self.actions.append(SentryLurk(self))

    def turn_changed(self):
        if self.board.current_turn == self.loyalty:
            self.jump_timer = max(0, self.jump_timer - 1)

    @property
    def sprite(self):
        if isinstance(self._sprite, tuple):
            return self._sprite[int(self.is_lurking)]
        return self._sprite
