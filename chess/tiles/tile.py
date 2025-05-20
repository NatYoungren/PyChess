import pygame as pg
import numpy as np
from typing import Optional, List, Union

from globalref import GlobalAccessObject

from utils.chess_types import PieceType, Vector, Position
from utils.chess_types import TileType, Loyalty, Direction, Vector

from utils.asset_loader import asset_loader as al


class Tile(GlobalAccessObject):
    position: Position
    sprite: Optional[object] # TODO: Use a sprite typealias or pg type or property?
    
    tiletype: TileType
    piece: Optional[PieceType]
    # objects: List[ChessObject] # TODO: implement?
    
    is_blocked: bool = False
    is_deadly: bool = False
    is_void: bool = False
    
    def __init__(self,
                 position: Position,
                 tiletype: TileType = TileType.DEFAULT,
                 sprite: Optional[pg.Surface] = None,
                 # TODO: Biome, which decides sprite based on terrain/coords/rng?
                 ):
    
        self.position: Position = position
        
        self.sprite = self.get_sprite(tiletype, position) if sprite is None else sprite
        
        self.tiletype: TileType = tiletype
        self.piece: Optional[PieceType] = None
        
        # self.objects: List[ChessObject] = [] # TODO: implement?
    
    # # TODO: Implement in subclasses?
    # def can_enter(self, piece: PieceType):
    #     return self.tiletype != TileType.WALL and self.tiletype != TileType.VOID
    
    # # Custom behavior based on tiletype
    # def enter(self, piece: PieceType):
    #     self.piece = piece # TODO: piece.tile = self?

    # def leave(self):
    #     self.piece = None # TODO: piece.tile = None?


    # def add_object(self, obj: ChessObject):
    #     self.objects.append(obj)
    
    # def remove_object(self, obj: Union[ChessObject, int, None]=None): # Remove with index?
    #     if obj is None:
    #         self.objects = [] # TODO: Delete them?
            
    #     elif isinstance(obj, int):
    #         if obj < 0 or obj >= len(self.objects):
    #             raise IndexError("Object index out of range.")
    #         self.objects.pop(obj)
            
    #     else:
    #         if obj not in self.objects:
    #             raise ValueError("Object not found in tile.")
            
    #     self.objects.remove(obj)
    
    def update(self):
        pass
    
    def __repr__(self):
        return f"Tile({self.position} : {self.tiletype.name}) -> ({self.piece})"# : {self.objects})"
    
    @classmethod
    def get_sprite(cls, tiletype: TileType, position: Position) -> pg.Surface:
        """
        Get the sprite for a given tile type and position.
        """
        sprite = al.tile_sprites.get(tiletype, None)
        if sprite is None:
            print(f"Warning: Tile sprite not found for tiletype {tiletype}. Using default sprite.")
            sprite = al.DEFAULT_TILE_SPRITE
        if isinstance(sprite, tuple) and len(sprite) == 2:
            sprite = sprite[int(position[0] % 2 == position[1] % 2)]
        return sprite