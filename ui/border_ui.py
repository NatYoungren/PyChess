import numpy as np
import pygame as pg
from typing import Dict, List, Union, Tuple, Callable, Optional


from utils.ui_utils import HEADER_FONT, STANDARD_FONT, THIN_FONT
from utils.ui_utils import render_text, sprite_transform
from utils.chess_types import Position, Vector, Loyalty

from utils.ui_utils import UIClickable, UIRegion

class TopBar(UIRegion):
    """
    Bar above the board containing ?.
    """
    scale: int # TODO: Remove?
        
    def __init__(self,
                 origin: Position,
                 size: Vector,
                 scale: int = 2,
                 ):        
        super().__init__(origin, size)
        self.scale: int = scale


class BottomBar(UIRegion):
    """
    Bar above the board containing ?.
    """
    scale: int # TODO: Remove?
    _leadership_pips: List[pg.Surface]
    
    def __init__(self,
                 origin: Position,
                 size: Vector,
                 scale: int = 2,
                 ):        
        super().__init__(origin, size)
        self.scale: int = scale
        
        # TODO: Does this need to be a clickable? (Map link??)
        battle_title = render_text('LEADERSHIP', STANDARD_FONT, scale=self.scale)
        title_pos = (self.origin[0] + self.size[0]//2 - battle_title.get_width()//2, self.origin[1] + 16)
        bt_clickable = UIClickable(title_pos, battle_title.get_size(), battle_title)
        self.add_clickable(bt_clickable)
        
        self._leadership_pips = []
        self._make_pips()

    def _make_pips(self, y: int = 24, size=(96, 64)):
        self._leadership_pips.clear()
        
        # idx = 0~empty, 1~full, 2~cost, 3~gain, 4~debt
        pip_sprites = self.al.indicator_sprites['pips']
        pip_sprites = tuple(sprite_transform(img, size=size) for img in pip_sprites)
        
        max_pips = self.ui.board.MAX_LEADERSHIP
        w = size[0] * max_pips
        x = (self.size[0] - w) // 2

        for i in range(max_pips):
            pip_clickable = UIClickable(self.origin+(x + i * size[0], y), size, sprite=pip_sprites)#, callback=callback)
            self._leadership_pips.append(pip_clickable)
            self.add_clickable(pip_clickable)

    def update_pips(self, leadership: int, delta: int = 0):
        """
        Update the leadership pip display.
        """
        # TODO: Implement 'debt' pips to show when cost is too high?
        for i, pip in enumerate(self._leadership_pips):
            if i < leadership: # Full or Cost
                pip._sprite_idx = 1 if i < leadership + delta else 2
                continue
            if i >= leadership: # Gain or empty
                pip._sprite_idx = 3 if i < leadership + delta else 0
                continue
