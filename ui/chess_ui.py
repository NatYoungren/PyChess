import os
import json
import numpy as np
import pygame as pg
from pygame import SRCALPHA, Color, Surface

from typing import Optional, Tuple, Union, Dict, List

import chess.chess_types as ct
from chess.chess_types import Loyalty, PieceType, TileType
from chess.chess_types import Position, Vector
from chess.chess_types import DirCls as D

from globalref import OBJREF

from chess.asset_loader import asset_loader as al # Move to objref?

# # #
# Load the graphics JSON configuration
graphics_config_file = os.path.join('config', 'graphics.json')
graphics_config = {}
with open(graphics_config_file, 'r') as f:
    graphics_config = json.load(f)
    # TODO: Store configs globally?
# # #

class ChessUI:
    """
    A singleton class for the chess UI.  
    This class is responsible for rendering the board, pieces, and effects.
    """
    # def __new__(cls): # TODO: Does this break with arguments??
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(ChessUI, cls).__new__(cls)
    #     return cls.instance

    @classmethod
    def from_config(cls, config=None, **kwargs):
        if config is None: config = graphics_config
        return cls(**{**config, **kwargs})
    
    def __init__(self,
                 window_width: int,
                 window_height: int,
                 tile_size: Union[int, Tuple[int, int]],
                 bg_color: Tuple[int, int, int],
                 window_title: str = 'PyChess',
                 **kwargs):
        
        self.window_size: Tuple[int, int] = (window_width, window_height)
        self._tile_size: int = tile_size
        self.bg_color: Tuple[int, int, int] = bg_color
        
        self.surf: Surface = pg.display.set_mode(self.window_size) # Window surface
        # self.bsurf: Surface = Surface(self.window_size) # Board surface
        # self.uisurf? # A surface for sidebars, only update every now and again?
        self.bsurf: Surface = Surface(self.window_size, flags=pg.SRCALPHA) # Board surface
        
        # self.psurf: Surface = Surface(self.window_size) # Preview surface?
        
        pg.display.set_caption(window_title)
        
        for k, v in kwargs.items():
            print('\tChessUI: Unrecognized config:', k, v)
    
    
    def draw(self):
        self.draw_background()
        self.draw_board()
        
        self.draw_tile_effects()
        self.draw_pieces()
        
        # if self.board.selected_tile is not None:
        #     self.draw_tile_effects()
            
        #     # if hovering: # TODO: Implement
        #     #     self.draw_preview()
        #     # else:
        #     self.draw_pieces()
        # else:
        #     self.draw_pieces()
        
        self.draw_ui()
        self.draw_cursor()
        
        self.surf.blit(self.bsurf, (0, 0))
        pg.display.flip()
    
    def draw_background(self):
        self.surf.fill(self.bg_color)
        self.bsurf.fill(Color(0, 0, 0, 0)) # Clear the board surface
    
    def draw_board(self):
        # tw, th = self.tile_size
        for t in self.board:
        # for w, h in np.ndindex(self.board.shape):
            # t = b[w, h]
            # x, y = t.position
            
            # TODO: TRANSFORM ONLY ONCE?
            #       Make .sprite a property which points to assetloader?
            img = self.sprite_transform(t.sprite, size=self.tile_size)
            self.b_blit(img, t.position)
            # self.surf.blit(img, (x*tw, y*th-(img.get_height()-th)))
        
    def draw_tile_effects(self):
        selected = self.board.selected_tile
        if selected is None: return
        # tw, th = self.tile_size
        # x, y = selected.position
        img = self.sprite_transform(img=np.random.choice(al.tile_effect_sprites['selected']),
                                    randomrotate=True,
                                    randomflip=True,
                                    size=self.tile_size)
        self.b_blit(img, selected.position)
        # self.surf.blit(img, (x*tw, y*th-(img.get_height()-th)))
        
        p = selected.piece
        if p is None: return
        # print(p.get_options())
        for (x, y), oc in p.get_options().items():
            match oc.name:
                case 'Move':
                    img = al.tile_effect_sprites['move']
                case 'Capture':
                    img = al.tile_effect_sprites['capture']
                case 'Castle':
                    img = al.tile_effect_sprites['misc']
                case _:
                    print('DRAWING VIABLE: Unknown outcome:', oc.name)
                    continue
            img = self.sprite_transform(img=img,
                                        randomrotate=True,
                                        randomflip=True,
                                        size=self.tile_size)
            self.b_blit(img, (x, y))

            # self.surf.blit(img, (x*tw, y*th-(img.get_height()-th)))
        
    def draw_pieces(self, exclude: Optional[list]=None):
        # tw, th = self.tile_size
        # All pieces in board positions
        for tile in self.board:
            p = tile.piece
            if p is None: continue
            if exclude is not None and p in exclude: continue
            
            # x, y = tile.position
            ratio = p.sprite.get_height() / p.sprite.get_width()
            img = self.sprite_transform(p.sprite, size=(self.tile_width, int(self.tile_width * ratio)))
            self.b_blit(img, tile.position)
            # self.surf.blit(img, (x*tw, y*th-(img.get_height()-th)))
    
    def draw_preview(self):
        # Currently-hovered outcome
        pass
    
    def draw_ui(self):
        # Buttons, text, menus
        pass
    
    def draw_cursor(self):
        pass
    
    def sprite_transform(self,
                         img: Surface,
                         randomflip: bool=False,
                         randomrotate: bool=False,
                         size: Union[None, int, Tuple[int, int]]=None) -> Surface:
        """
        Transform a sprite to the given size.
        """
        if randomflip: img = pg.transform.flip(img, *np.random.randint(0, 2, 2))
        if randomrotate: img = pg.transform.rotate(img, np.random.randint(0, 4)*90)
        if size is not None:
            if isinstance(size, int): size = (size, size)
            img = pg.transform.scale(img, size)
        return pg.transform.scale(img, size)
    
    # TODO: Method to refresh the 
    
    
    def b_blit(self, img: Surface, pos: Position):
        """
        Blit an image to the board surface.
        """
        x, y = pos
        tw, th = self.tile_size
        self.bsurf.blit(img, self.board_origin + (x*tw, y*th-(img.get_height()-th)))
    
    @property
    def board(self) -> object: # TODO: Give more classes getters like this.
        return OBJREF.BOARD
    
    
    @property
    def width(self) -> int:
        return self.window_size[0]
    @property
    def height(self) -> int:
        return self.window_size[1]
    
    @property
    def b_size(self) -> Tuple[int, int]:
        return self.b_width, self.b_height
    @property
    def b_width(self) -> Union[int, Tuple[int, int]]:
        return self.tile_width * self.board.width
    @property
    def b_height(self) -> Union[int, Tuple[int, int]]:
        return self.tile_height * self.board.height
    
    @property
    def tile_size(self) -> tuple:
        return self._tile_size if isinstance(self._tile_size, tuple) else (self._tile_size, self._tile_size)
    @property
    def tile_width(self) -> int:
        return self.tile_size[0]
    @property
    def tile_height(self) -> int:
        return self.tile_size[1]
    
    # TODO: Allow board origin to be scrolled w/ right click!
    @property
    def board_origin(self) -> Vector:
        # width, tile_width*board.width
        return np.array(((self.width - self.b_width) // 2, \
                        (self.height - self.b_height) // 2))
        # return Vector(0, 0)
    
    
    # TODO: Implement this and call when window is resized or board is zoomed/resized.
    # def update_board_origin(self, x: int, y: int):
    #     self.board_origin = Vector(x, y)