

import pygame as pg
from typing import Dict, List, Union, Tuple, Callable, Optional


from utils.ui_utils import HEADER_FONT, STANDARD_FONT, THIN_FONT
from utils.ui_utils import render_text, sprite_transform
from utils.chess_types import Position, Vector, Loyalty

from utils.ui_utils import UIClickable, UIRegion

from utils.asset_loader import asset_loader as al

class TopBar(UIRegion):
    """
    Bar above the board containing ?.
    """
    ui: object
    scale: int # TODO: Remove?
        
    def __init__(self,
                 ui,
                 scale: int = 2, # TODO: Remove?
                 ):
        origin = (ui.b_origin[0], 0)
        size = (ui.b_size[0], ui.b_origin[1])
        
        super().__init__(origin, size)
        self.ui = ui
        self.scale: int = scale




class BottomBar(UIRegion):
    """
    Bar above the board containing ?.
    """
    ui: object
    scale: int # TODO: Remove?
    
    _leadership_pips: List[pg.Surface]
    NUM_PIPS: int = 5
    
    
    def __init__(self,
                 ui,
                 scale: int = 2, # TODO: Remove?
                 ):
        origin = (ui.b_origin[0], ui.b_origin[1] + ui.b_size[1])
        size = (ui.b_size[0], ui.height - origin[1])
        
        super().__init__(origin, size)
        self.ui = ui
        self.scale: int = scale
        
        # TODO: Does this need to be a clickable? (Map link??)
        battle_title = render_text('Leadership', STANDARD_FONT, scale=self.scale)
        title_pos = (self.origin[0] + self.size[0]//2 - battle_title.get_width()//2, self.origin[1] + 16)
        bt_clickable = UIClickable(title_pos, battle_title.get_size(), battle_title)
        self.add_clickable(bt_clickable)
        
        self._leadership_pips = []
        self._make_pips()

    def _make_pips(self, y: int = 24, size=(96, 64)):
        # Empty, full, cost, gain
        pip_sprites = al.indicator_sprites['pips']
        pip_sprites = tuple(sprite_transform(img, size=size) for img in pip_sprites)
        
        w = size[0] * self.NUM_PIPS
        x = (self.size[0] - w) // 2
        import numpy as np

        for i in range(self.NUM_PIPS):
            def callback(p):
                print(f"Clicked pip {i}: {p}")
                return self.update_pips(np.random.randint(0, 6), delta=np.random.randint(-3, 4))
            pip_clickable = UIClickable(self.origin+(x + i * size[0], y), size, sprite=pip_sprites, callback=callback)
            self._leadership_pips.append(pip_clickable)
            self.add_clickable(pip_clickable)

    def update_pips(self, leadership: int, delta: int = 0):
        """
        Update the leadership pip display.
        """
        for i, pip in enumerate(self._leadership_pips):
            if i < leadership: # Full or Cost
                pip._sprite_idx = 1 if i < leadership + delta else 2
                continue
            if i >= leadership: # Gain or empty
                pip._sprite_idx = 3 if i < leadership + delta else 0
                continue
