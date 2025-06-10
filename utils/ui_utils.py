import pygame as pg
import numpy as np
from typing import Optional, Union, Tuple, Dict, List, Callable, Self

from utils.chess_types import Position, Vector


pg.font.init()
MHEADER_FONT = pg.font.Font("assets/fonts/merlin-16x16-monospaced.ttf", 16)
MSTANDARD_FONT = pg.font.Font("assets/fonts/merlin-8x8-monospaced.ttf", 8)
MTHIN_FONT = pg.font.Font("assets/fonts/merlin-light-8x8-monospaced.ttf", 8)

HEADER_FONT = pg.font.Font("assets/fonts/merlin-16x16.ttf", 16)
STANDARD_FONT = pg.font.Font("assets/fonts/merlin-8x8.ttf", 8)
THIN_FONT = pg.font.Font("assets/fonts/merlin-light-8x8.ttf", 8)



def render_text(text: str,
                font: pg.font.Font = STANDARD_FONT,
                color: Union[pg.Color, Tuple[int, int, int]] = (255, 255, 255),
                scale: Optional[int] = None) -> pg.Surface:
    """
    Render text to a surface.
    """
    
    text_surface = font.render(text, True, color)
    if scale is not None:
        text_surface = pg.transform.scale(text_surface,
                                          (text_surface.get_width() * scale,
                                           text_surface.get_height() * scale))
    return text_surface


def sprite_transform(img: pg.Surface,
                     randomflip: bool = False,
                     randomrotate: bool = False,
                     rotate_by: Optional[int] = None,
                     size: Union[None, int, Tuple[int, int]] = None) -> pg.Surface:
    """
    Transform a sprite to the given size (optionally flipped or rotated).
    """
    if randomflip: img = pg.transform.flip(img, *np.random.randint(0, 2, 2))
    if randomrotate:
        img = pg.transform.rotate(img, np.random.randint(0, 4)*90)
    
    elif isinstance(rotate_by, (int, np.int64)):
        img = pg.transform.rotate(img, rotate_by*90)
        
    if size is not None:
        if isinstance(size, (int, np.int64)):
            size = (size, size)
        img = pg.transform.scale(img, size)
    
    return img

# UI Base Classes

class UIClickable(GlobalAccessObject):
    """
    Simple class for clickable buttons/sprites/text.  
    Can be provided with a callback function.
    """
    _origin: Position
    _size: Vector
    _sprites: Union[None, pg.Surface, Tuple[pg.Surface, ...]]
    _hsprites: Union[None, pg.Surface, Tuple[pg.Surface, ...]]
    _sprite_offset: Vector
    _callback: Callable
    
    # TODO: Consider inheriting from sprite or spritegroup?
    _sprite_idx: int = 0  # For tuple sprites, to keep track of which sprite to show.
    
    def __init__(self,
                 origin: Position,
                 size: Vector,
                 sprite: Union[None, pg.Surface, Tuple[pg.Surface, ...]] = None,
                 hsprite: Union[None, pg.Surface, Tuple[pg.Surface, ...]] = None,
                 sprite_offset: Vector = (0, 0),
                 callback: Callable = lambda _: None,
                 sprite_idx: int = 0):
        self._origin = np.array(origin)
        self._size = np.array(size)
        self._sprites = (sprite,) if type(sprite) is pg.Surface else sprite
        self._hsprites = self._sprites if hsprite is None else (hsprite,) if type(hsprite) is pg.Surface else hsprite
        self._sprite_offset = np.array(sprite_offset)
        self._callback = callback
        self._sprite_idx = sprite_idx
        
        self._hovered: bool = False
        if len(self.sprites) != len(self.hsprites):
            print(self.__class__.__name__, f"WARNING: Sprites ({len(self.sprites)}) and hover sprites ({len(self.hsprites)}) must have the same length.")
    
    def draw(self, surf: pg.Surface, hovered: Optional[Self]=None): # TODO: Hovered arg override? Bool or Clickable reference?
        s = self.sprite if not self == hovered else self.hsprite
        if s is None: return
        # NOTE: Tuples require custom implementation.
        surf.blit(s, self.sprite_pos) # TODO: What could area argument do?
    
    def at_pos(self, pos: Position):
        return self.origin[0] <= pos[0] <= self.origin[0] + self.size[0] and \
               self.origin[1] <= pos[1] <= self.origin[1] + self.size[1]
        
    def get_hovered(self, pos: Position) -> Optional[Self]:
        return self if self.at_pos(pos) else None
    
    # TODO: Rework to have UI track the hovered clickable.
    #       Click should just 'click' the hovered clickable from inputhandler without searching.
    def click(self, pos: Position = None, m1: bool = True, m2: bool = False):
        """ Trigger callback if clicked. """
        if pos is None or self.at_pos(pos): self.callback(self)
    
    @property
    def sprite_pos(self):
        return self.origin + self.sprite_offset
    @property
    def origin(self):
        return self._origin
    @property
    def size(self):
        return self._size
    @property
    def sprite(self):
        return self.sprites[self.sprite_idx] # TODO: Index error handling?
    @property
    def hsprite(self):
        return self.hsprites[self.sprite_idx] # TODO: Index error handling?
    @property
    def sprites(self):
        return self._sprites if isinstance(self._sprites, tuple) else (self._sprites,)
    @property
    def hsprites(self):
        return self._hsprites if isinstance(self._hsprites, tuple) else (self._hsprites,)
    @property
    def sprite_offset(self):
        return self._sprite_offset
    @property
    def callback(self):
        return self._callback
    @property
    def sprite_idx(self):
        return self._sprite_idx


class UIRegion(UIClickable):
    clickables: List[UIClickable]
    
    def __init__(self,
                 origin: Position,
                 size: Vector,
                 sprite: Union[None, pg.Surface, Tuple[pg.Surface, ...]] = None,
                 hsprite: Union[None, pg.Surface, Tuple[pg.Surface, ...]] = None,
                 sprite_offset: Vector = (0, 0),
                 callback: Callable = lambda _: None):
        super().__init__(origin=origin, size=size,
                         sprite=sprite, hsprite=hsprite,
                         sprite_offset=sprite_offset, callback=callback)
        self.clickables = []
    
    def draw(self, surf: pg.Surface, hovered: Optional[Self]=None):
        super().draw(surf, hovered=hovered)
        for cl in self.clickables:
            cl.draw(surf, hovered=hovered)
    
    def add_clickable(self, clickable: UIClickable):
        self.clickables.append(clickable)
    
    # TODO: Rename update hovered?
    def get_hovered(self, pos: Position) -> Optional[UIClickable]:
        """
        Check if any clickable is hovered at the given position.
        Returns the first hovered clickable or None.
        """
        # if not super().at_pos(pos): return None # TODO: Remove?
        for cl in self.clickables:
            hov = cl.get_hovered(pos)
            if hov is not None:
                return hov
        return None
    
    def click(self, pos: Position = None, m1: bool = True, m2: bool = False):
        """
        Trigger callback if clicked.
        If a clickable is hovered, trigger its callback instead.
        """
        cl = self.get_hovered(pos)
        if cl is not None:
            cl.click(pos, m1, m2)
        # TODO: Trigger callback if hovered but no subclickable?
