import os
import json
import numpy as np
import pygame as pg
from pygame import SRCALPHA, Color, Surface
from typing import Optional, Tuple, Union, Dict, List


from globalref import GlobalAccessObject


import utils.chess_types as ct
from utils.chess_types import Loyalty, PieceType, TileType
from utils.chess_types import Position, Vector
from utils.chess_types import DirCls as D

from chess.actions.action import Action
from chess.actions.outcome import Outcome
from chess.tiles.tile import Tile
from chess.units.piece import ChessPiece


from utils.ui_utils import sprite_transform
from utils.asset_loader import asset_loader as al # Move to objref?

# # #
# Load the graphics JSON configuration
graphics_config_file = os.path.join('config', 'graphics.json')
graphics_config = {}
with open(graphics_config_file, 'r') as f:
    graphics_config = json.load(f)
    # TODO: Store configs globally?
# # #

class ChessUI(GlobalAccessObject):
    """
    Singleton object which handles chess game UI.  
    This class is responsible for rendering the board, pieces, and effects.
    """

    @classmethod
    def from_config(cls, config=None, **kwargs):
        if config is None: config = graphics_config
        return cls(**{**config, **kwargs})
    
    # Graphics config
    fps: int
    window_size: Tuple[int, int]
    _tile_size: Union[int, Tuple[int, int]]
    bg_color: Tuple[int, int, int]
    
    # Pygame surfaces
    surf: Surface
    bsurf: Surface

    # Selected tile
    s_tile: Optional[Tile]
    
    # Hovered tile
    h_tile: Optional[Tile]
    
    # Frame counter
    frame: int
    _hide_cursor: bool = False
    
    def __init__(self,
                 fps: int = 60,
                 hide_cursor: bool = False,
                 tile_size: Union[int, Tuple[int, int]] = 65,
                 window_width: int = 1280,
                 window_height: int = 720,
                 bg_color: Tuple[int, int, int] = (0, 0, 0),
                 window_title: str = 'PyChess',
                 **kwargs):
        
        self.fps: int = fps
        self.window_size: Tuple[int, int] = (window_width, window_height)
        self._tile_size: Union[int, Tuple[int, int]] = tile_size
        self.bg_color: Tuple[int, int, int] = bg_color
        
        # TODO: Have window surf exist globally, and just write to it?
        self.surf: Surface = pg.display.set_mode(self.window_size) # Window surface
        self.bsurf: Surface = Surface(self.window_size, flags=pg.SRCALPHA) # Board surface
        # self.uisurf? # A surface for sidebars, only update every now and again?
        # self.psurf: Surface = Surface(self.window_size) # Preview surface?
        
        pg.display.set_caption(window_title)
        
        self.hide_cursor: bool = hide_cursor
        
        for k, v in kwargs.items():
            print('\tChessUI: Unrecognized config:', k, v)
        
        # TODO: property for protected field?
        self.s_tile: Optional[Tile] = None
        self.h_tile: Optional[Tile] = None
        self.frame: int = 0
    
    def draw(self):
        self.draw_background()
        self.draw_tiles()
        
        self.draw_tile_effects()
        self.draw_pieces()
        
        self.draw_moodles()
        
        self.draw_ui()
        
        self.surf.blit(self.bsurf, (0, 0))
        self.draw_cursor()

        pg.display.flip()
        
        self.frame += 1
    
    def draw_background(self):
        self.surf.fill(self.bg_color)
        self.bsurf.fill(Color(0, 0, 0, 0)) # Clear the board surface
    
    def draw_tiles(self):
        for t in self.board:
            # TODO: TRANSFORM ONLY ONCE?
            #       Make .sprite a property which points to assetloader?
            img = sprite_transform(t.sprite, size=self.tile_size)
            self.b_blit(img, t.position)
        
    def draw_tile_effects(self):
        self.draw_selected()
        self.draw_hover()

    def draw_selected(self):
        # Draw effects on selected + outcome tiles
        if self.s_piece is None: return
            
        # Selected tile effect
        img = al.tile_effect_sprites['selected']
        img = sprite_transform(img=img,
                               rotate_by=self.frame//(self.fps//4),
                               size=self.tile_size)
        self.b_blit(img, self.s_pos)
        
        # Draw outcome tile effects
        for t, oc in self.s_piece.outcomes.items():
            img = oc.get_effect()
            if img is not None:
                self.b_blit(img, t.position)
            else:
                print(f'TILE_EFFECT: No effect for outcome:', oc.name)
                continue
            
    def draw_hover(self):
        # Draw effects on hovered tile (scrolling effect on hovered outcomes)
        if self.h_tile is None: return
        if self.h_tile == self.s_tile: return
        
        # Draw outcome hover effects
        if self.s_piece is not None and self.h_tile in self.s_piece.outcomes.keys():
            if self.h_tile in self.s_piece.outcomes.keys():
                oc: Outcome = self.s_piece.outcomes[self.h_tile]
                img = oc.get_hover_effect()
                if img is not None:
                    self.b_blit(img, self.h_pos)
                else:
                    print(f'TILE_EFFECT: No hover effect for outcome:', oc.name)
                    
        # Draw non-outcome hover effect
        else:
            img = al.tile_effect_sprites['hover'][self.frame//(self.fps)%len(al.tile_effect_sprites['hover'])]
            img = sprite_transform(img=img,
                                   rotate_by=self.frame//(self.fps//4),
                                   size=self.tile_size)
            self.b_blit(img, self.h_pos)


    def draw_pieces(self, exclude: Optional[list]=None):
        # All pieces on board
        for tile in self.board:
            p = tile.piece
            if p is None: continue
            if exclude is not None and p in exclude: continue
            
            ratio = p.sprite.get_height() / p.sprite.get_width()
            img = sprite_transform(p.sprite, size=(self.tile_width, int(self.tile_width * ratio)))
            self.b_blit(img, tile.position)
    
    def draw_moodles(self):
        
        # Check moodles
        moodle_sprites = al.icon_sprites['moodle']
        check_moodles = moodle_sprites['check']
        for (checkee, checker, oc) in self.board._checks:
            if checker.loyalty in (Loyalty.WHITE, Loyalty.WHITE_AUTO):
                img = check_moodles[0]
            else:
                img = check_moodles[1]
            img = sprite_transform(img, size=self.tile_size)
            self.b_blit(img, checker.position)
            
    
    def draw_preview(self):
        # Currently-hovered outcome
        pass
    
    def draw_ui(self):
        # Buttons, text, menus
        pass
    
    def draw_cursor(self):
        if not self.hide_cursor: return # If using system cursor, don't draw.
        x, y = self.ih.m_pos#pg.mouse.get_pos()
        # x, y = self.m_pos
        if pg.mouse.get_pressed()[0]:
            img = al.cursor_sprites['click']
        elif self.h_piece is not None:
            img = al.cursor_sprites['hover']
        else:
            img = al.cursor_sprites['default']
            
        img = pg.transform.scale(img, (self.tile_width//2, self.tile_height//2))
        self.surf.blit(img, (x - img.get_width()//2.25, y - img.get_height()//5))
    
    
    # TODO: Method to refresh tile effects?
    
    def b_blit(self, img: Surface, pos: Position):
        """
        Blit an image to the board surface.
        """
        x, y = pos
        tw, th = self.tile_size
        self.bsurf.blit(img, self.b_origin + (x*tw, y*th-(img.get_height()-th)))
    
    # Selection get/set
    @property
    def s_pos(self) -> Position:
        return self.s_tile.position if self.s_tile is not None else None
    @s_pos.setter # TODO: Deprecate?
    def s_pos(self, value: Position):
        self.s_tile = self.board.get_tile(value)
    @property
    def s_piece(self) -> Optional[ChessPiece]:
        return self.s_tile.piece if self.s_tile is not None else None
    @s_piece.setter # TODO: Deprecate?
    def s_piece(self, value: ChessPiece):
        self.s_tile = self.board.get_tile(value.position)
    
    # Hover get/set
    @property
    def h_pos(self) -> Position:
        return self.h_tile.position if self.h_tile is not None else None
    @h_pos.setter # TODO: Deprecate?
    def h_pos(self, value: Position):
        self.h_tile = self.board.get_tile(value)
    @property
    def h_piece(self) -> Optional[ChessPiece]:
        return self.h_tile.piece if self.h_tile is not None else None
    @h_piece.setter # TODO: Deprecate?
    def h_piece(self, value: ChessPiece):
        self.h_tile = self.board.get_tile(value.position)
    
    # Window properties
    @property
    def width(self) -> int:
        return self.window_size[0]
    @property
    def height(self) -> int:
        return self.window_size[1]
    
    # Board properties
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
    def b_origin(self) -> Vector:
        """ Pixel coordinates of top-left corner of board. """
        # TODO: Allow board origin to be scrolled w/ right click?
        # TODO: Implement event response which readjusts board origin when window size changes.
        return np.array(((self.width - self.b_width) // 2, \
                        (self.height - self.b_height) // 2))

    # Tile properties
    @property
    def tile_size(self) -> tuple:
        return self._tile_size if isinstance(self._tile_size, tuple) else (self._tile_size, self._tile_size)
    @property
    def tile_width(self) -> int:
        return self.tile_size[0]
    @property
    def tile_height(self) -> int:
        return self.tile_size[1]
    
    # Display properties
    @property
    def hide_cursor(self) -> bool:
        return self._hide_cursor
    @hide_cursor.setter
    def hide_cursor(self, value: bool):
        self._hide_cursor = value
        if value:
            pg.mouse.set_visible(False)
            pg.mouse.set_pos(self.width // 2, self.height // 2)
        else:
            pg.mouse.set_visible(True)
    
    
    # TODO: Remove or rework.
    def draw_tile_edges(self):
        for t in self.board:
            # TODO: This is a total clusterfuck, but it KINDA works.
            #       Needs half-tiles or a one-gap edge tile.
            
            # Draw an edge for the tile above
            if t.tiletype == TileType.VOID:
                t1 = self.board.get_tile(t.position - D.f)
                if t1 is not None and t1.tiletype != TileType.VOID:
                    flt = self.board.get_tile(t.position - D.f_l)
                    lt = self.board.get_tile(t.position - D.l)
                    frt = self.board.get_tile(t.position - D.f_r)
                    rt = self.board.get_tile(t.position - D.r)
                    # print(t.tiletype, t1.tiletype, flt.tiletype, lt.tiletype, frt.tiletype, rt.tiletype)
                    cont_left = flt is not None and flt.tiletype != TileType.VOID and (lt is None or lt.tiletype == TileType.VOID)
                    cont_right = frt is not None and frt.tiletype != TileType.VOID and (rt is None or rt.tiletype == TileType.VOID)
                    if cont_left and cont_right:
                        img = al.tile_sprites[TileType.VOID]['center']
                    elif cont_left:
                        img = al.tile_sprites[TileType.VOID]['right']
                    elif cont_right:
                        img = al.tile_sprites[TileType.VOID]['left']
                    img = sprite_transform(img, size=self.tile_size)
                    self.b_blit(img, t.position)
                    