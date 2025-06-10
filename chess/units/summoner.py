import numpy as np

from utils.chess_types import Position, Vector
from utils.chess_types import DirCls as D
from utils.chess_types import Loyalty, PieceType

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
                self.add_outcome(t, Move(self.piece, pos))

    
class SummonerSummon(Action):
    """
    Represents a zombie summoning action for a summoner.
    """
    summon_loyalty: Loyalty = Loyalty.NONE
    def __init__(self, piece):
        super().__init__(piece)
        if self.piece.loyalty != Loyalty.NONE and self.piece.loyalty.value % 1 == 0:
            self.summon_loyalty = Loyalty(self.piece.loyalty.value - 0.5)
            
    def update(self):
        super().update()
        
        for v in (D.r, D.l):
            pos, t, p = self.at_vec(v)
            if t is None: continue
            if t.is_blocked: continue # Blocked tile
            if t.is_void: continue # Void tile
            if p is not None: continue # Blocked by piece
            # print('Summon:', pos)
            self.add_outcome(t, Summon(self.piece, pos, Zombie, self.summon_loyalty))
            
class Summoner(ChessPiece):
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.SUMMONER, position=position)
        self.actions.append(SummonerMove(self))
        self.actions.append(SummonerSummon(self))


class ZombieMove(Action):
    def update(self, retry:bool=True):
        super().update()
        for v in (D.f,):
            for pos, t, p in self.get_line(v, length=1, enemy_ok=True, ally_ok=True):
                if t is None or t.is_void or t.is_blocked: continue
                self.outcomes[t] = Move(self.piece, pos) if p is None else Capture(self.piece, pos, p)
        if not self.outcomes:
            # print('ZombieMove: no outcomes')
            if retry:
                # print('ZombieMove: retrying')
                self.piece.change_facing()
                self.update(retry=False)

# TODO: Zombies should die when summoner dies?
class Zombie(ChessPiece):
    def __init__(self, loyalty: Loyalty, position, facing: Vector=None):
        # Shift to 'auto' loyalty
        # TODO: Improve this to not be kinda wonky.
        super().__init__(loyalty=loyalty, piece_type=PieceType.ZOMBIE, position=position)
        self.actions.append(ZombieMove(self))

    def change_facing(self, sight_range: int=7):
        # TODO: Remove 'sight' it is confusing.
        # Left zombies should always turn 90 degrees right?
        # Right zombies should always turn 90 degrees left?
        print("USING SHITTY ZOMBIE FACING FUNCTION")
        dirs = D.cardinal
        priority = np.zeros(len(dirs), dtype=int)
        
        for i, v in enumerate(dirs):
            if np.all(self.orient_vector(v) == self.facing): continue
            l = self.get_line(v, length=7, enemy_ok=True, ally_ok=True)
            if not l:
                # print('no line:', v)
                continue
            pos, t, p = l[-1]
            if p is None:
                # print('no piece:', v)
                continue
            priority[i] = sight_range-len(l)
            # print('line:', v, l)
        
        # print('changing facing:', priority)
        dir_p = dirs[np.argmax(priority)]
        self.facing = self.orient_vector(dir_p)
        # print('new facing:', self.facing)
