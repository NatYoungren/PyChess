import pygame as pg
import numpy as np
from typing import Dict, Optional, Self, Union, Tuple, Callable, List

from utils.chess_types import Position, Vector, Direction
from utils.chess_types import Loyalty, PieceType
from utils.chess_types import DirCls as D

from globalref import GlobalAccessObject

from utils.ui_utils import sprite_transform
from utils.asset_loader import asset_loader as al
# from chess.units.get_piece import get_piece_class


# TODO: Add 'captured pieces' property to outcomes.
#       This way an outcome doesn't need to be a 'capture' to be flagged as such.



class Outcome(GlobalAccessObject):
    """
    Represents a change in board state.
    """
    
    name: str
    piece: object
    callback: Callable
    morale_cost: int = 0
    leadership_cost: int = 0
    end_turn: bool = True
    
    # TODO: Store some info that could be used to preview the action?
    # prev_dict: Dict[Piece, Optional[Position]] = {}
    # TODO: Could also contain code to render this preview?
    #       With a lerp value?
    
    _effect_sprite: Union[pg.Surface, None]
    _hover_sprites: Union[Tuple[pg.Surface], None]
    
    def __init__(self, piece, callback: Callable=lambda: None, **kwargs):
        self.name = self.__class__.__name__
        self.piece = piece
        self.callback = callback
    
    def realize(self) -> bool:
        """
        Apply this outcome to the board state.
        Returns True if the turn should end.
        """
        self.callback() # TODO: Args? Kwargs?
        return self.end_turn
    
    # TODO: This would be neat.
    def preview(self, surf, lerp: float):
        """
        Preview the action.
        """
        pass
    
    def get_effect(self) -> Optional[pg.Surface]: # TODO: Add override arguments for board/ui?
        """
        Get the tile effect sprite for this outcome.
        """
        if self._effect_sprite is None: return None
        ui = self.ui
        img = sprite_transform(img=self._effect_sprite,
                               rotate_by=ui.frame//(ui.fps//4),
                               size=ui.tile_size)
        return img
    
    def get_hover_effect(self) -> Optional[pg.Surface]:
        if self._hover_sprites is None: return None
        ui = self.ui
        img = self._hover_sprites[ui.frame//(ui.fps//4)%len(self._hover_sprites)]
        img = sprite_transform(img=img, size=ui.tile_size)
        return img



class Move(Outcome):
    target: Position
    
    LERP_MAX: float = 0.5 # TODO: Make this a constant?
    
    _effect_sprite = al.tile_effect_sprites['Move']
    _hover_sprites = al.tile_effect_sprites['blinds']['Move']

    def __init__(self, piece, target: Position, **kwargs):
        super().__init__(piece=piece, **kwargs)
        self.target = target
    
    def realize(self):
        self.piece.move(self.target)
        return super().realize()
    
    def preview(self, surf, lerp: float):
        pass
        
class Capture(Move):
    captured: object
    
    _effect_sprite = al.tile_effect_sprites['Capture']
    _hover_sprites = al.tile_effect_sprites['blinds']['Capture']

    def __init__(self, piece, target: Position, captured: Union[object, Tuple[object]], **kwargs):
        super().__init__(piece=piece, target=target, **kwargs)
        self.captured = captured if isinstance(captured, tuple) else (captured,)
    
    def realize(self):
        for p in self.captured:
            t = self.board.get_tile(p.position)
            t.piece = None
        return super().realize()
        


class Promote(Move): # TODO: Could be capture???
    promoted_to: PieceType
    def __init__(self, piece, target: Position, promoted_to: PieceType = PieceType.QUEEN, **kwargs):
        super().__init__(piece=piece, target=target, **kwargs)
        self.promoted_to = promoted_to
        
    def realize(self):
        t = self.board.get_tile(self.target)
        # Add method to board?
        print("REMOVED DUE TO CIRCULAR IMPORT ISSUE.")
        # new_piece = get_piece_class(self.promoted_to)(board, self.piece.loyalty, self.target)
        # t.piece = new_piece
        return super().realize()



class Castle(Outcome):
    rook_piece: object
    
    _effect_sprite = al.tile_effect_sprites['Castle']
    _hover_sprites = al.tile_effect_sprites['blinds']['Castle']

    
    def __init__(self, king_piece, rook_piece, **kwargs):
        super().__init__(piece=king_piece, **kwargs)
        # NOTE: self.piece is the king piece.
        self.rook_piece = rook_piece
    
    def realize(self):
        # TODO: Should we really care if the king is in check?
        vec = self.rook_piece.position - self.piece.position
        vec = vec // abs(sum(vec)) # NOTE: Should work because it is a cardinal vector
        self.piece.move(self.piece.position + vec*2)
        self.rook_piece.move(self.piece.position - vec)
        return super().realize()


class Summon(Outcome):
    piece: object
    target: Position
    summoned: object
    summon_loyalty: Loyalty
    
    _effect_sprite = al.tile_effect_sprites['Summon']
    _hover_sprites = al.tile_effect_sprites['blinds']['Summon']

    def __init__(self, piece, target: Position, summoned: type, loyalty: Optional[Loyalty] = None, **kwargs):
        super().__init__(piece=piece, **kwargs)
        self.target = target
        self.summoned = summoned
        self.summon_loyalty = loyalty if loyalty is not None else self.piece.loyalty
    
    def realize(self):
        t, p = self.board.at_pos(self.target)
        if p is not None: # TODO: Debug, remove eventually.
            raise ValueError("CANNOT SUMMON: Board is occupied.")
        t.piece = self.summoned(loyalty=self.summon_loyalty, position=self.target)
        return super().realize()
