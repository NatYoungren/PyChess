import numpy as np

from chess.chess_types import Position, Vector
from chess.chess_types import DirCls as D
from chess.chess_types import Loyalty, PieceType

from chess.units.piece import ChessPiece
from chess.actions.action import Action
from chess.actions.outcome import Move, Capture, Summon

class SummonerMove(Action):
    """
    Represents a move/capture action for a summoner.
    """
    def update(self):
        super().update()
        
        for v in (D.f_l, D.f_r, D.b):
            for pos, t, p in self.get_line(v, length=1, enemy_ok=False):
                if t is None: continue
                self.outcomes[t] = Move(self.piece, pos)
    
class SummonerSummon(Action):
    """
    Represents a zombie summoning action for a summoner.
    """
    def update(self):
        super().update()
        
        for v in (D.r, D.l):
            pos, t, p = self.at_vec(v)
            if t is None: continue
            if t.is_blocked: continue # Blocked tile
            if t.is_void: continue # Void tile
            if p is not None: continue # Blocked by piece
            # print('Summon:', pos)
            self.outcomes[t] = Summon(self.piece, pos, Zombie)
            
class Summoner(ChessPiece):
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.SUMMONER, position=position)
        self.actions.append(SummonerMove(self))
        self.actions.append(SummonerSummon(self))



class ZombieMove(Action):
    def update(self):
        super().update()
        for v in (D.f,):
            for pos, t, p in self.get_line(v, length=1, enemy_ok=True, ally_ok=True):
                if t is None: continue
                self.outcomes[t] = Move(self.piece, pos) if p is None else Capture(self.piece, pos, p)

# TODO: Zombies should die when summoner dies?
class Zombie(ChessPiece):
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.ZOMBIE, position=position)
        self.actions.append(ZombieMove(self))
