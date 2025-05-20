import os
import pygame as pg

from utils.chess_types import Loyalty, PieceType, TileType

# TODO: Rename to 'asset manager'
#       Add to OBJREF
class AssetLoader:
    """
    A class to load and manage assets for the chess game.
    """
    def __new__(cls): # https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/#
        if not hasattr(cls, 'instance'):
            cls.instance = super(AssetLoader, cls).__new__(cls)
        return cls.instance
    
    PIECE_SPRITE_DIRECTORY = os.path.join('assets', 'units')
    PIECE_SPRITE_FILES = {
        Loyalty.WHITE: {
            PieceType.PAWN: "W_Pawn.png",
            PieceType.KNIGHT: "W_Knight.png",
            PieceType.BISHOP: "W_Bishop.png",
            PieceType.ROOK: "W_Rook.png",
            PieceType.QUEEN: "W_Queen.png",
            PieceType.KING: "W_King.png",
            PieceType.SUMMONER: "Summoner1.png",
            PieceType.JESTER: ("Jester1.png", "Jester2.png"),
            },
        Loyalty.WHITE_AUTO: {
            PieceType.ZOMBIE: "Zombie1.png",
        },

        Loyalty.BLACK: {
            PieceType.PAWN: "B_Pawn.png",
            PieceType.KNIGHT: "B_Knight.png",
            PieceType.BISHOP: "B_Bishop.png",
            PieceType.ROOK: "B_Rook.png",
            PieceType.QUEEN: "B_Queen.png",
            PieceType.KING: "B_King.png",
            PieceType.SUMMONER: "Summoner2.png",
            PieceType.JESTER: ("Jester3.png", "Jester4.png"),
        },
        Loyalty.BLACK_AUTO: {
            PieceType.ZOMBIE: "Zombie2.png",
        },
        
        # TODO: Find better solution.
        Loyalty.NONE: {
            PieceType.NONE: "defaultpiece.png",
        }
    }
    
    # BOARD_SPRITE_DIRECTORY = os.path.join('assets', 'boards')
    # BOARD_SPRITE_FILES = {
    #     1: "board_plain_01.png",
    #     2: "board_plain_02.png",
    #     3: "board_plain_03.png",
    #     4: "board_plain_04.png",
    #     5: "board_plain_05.png",
    # }

    
    TILE_SPRITE_DIRECTORY = os.path.join('assets', 'tiles')
    TILE_SPRITE_FILES = {
        TileType.VOID: (
            "tiles5.png",
            "tiles6.png"
        ),
            
        #     "center": "tiles6.png", # TODO: Use these on top of VOID tiles, to show perspective/bottom of normal tiles.
        #     "right": "tiles7.png",  #
        #     "left": "tiles8.png",   #
        
        TileType.FLOOR: (
            "tiles1.png",
            "tiles2.png",
        ),
        # TileType.WALL: "wall.png", # TODO: Add wall sprite.
        TileType.WALL: (
            "tiles3.png",
            "tiles4.png",
        ),
        TileType.CHASM: (
            "tiles7.png",
            "tiles8.png",
        ),
        TileType.DEFAULT: "default_tile.png"
    }
    
    TILE_EFFECT_SPRITE_DIRECTORY = os.path.join('assets', 'tile_effects')
    TILE_EFFECT_SPRITE_FILES = { # TODO: Create enums for outcomes?
        'Move': "tile_effects1.png",
        'Capture': "tile_effects2.png",
        'Castle': 'tile_effects5.png',
        'Summon': 'tile_effects6.png',

        'hover': (
            "tile_effects3.png",
            "tile_effects4.png",
        ),
        
        'selected' : 'tile_effects7.png',
        
        'blinds': {
            'Move': ('tile_effect_blinds1.png',
                     'tile_effect_blinds2.png',
                     'tile_effect_blinds3.png'),
            'Capture': ('tile_effect_blinds4.png',
                        'tile_effect_blinds5.png',
                        'tile_effect_blinds6.png'),
            'Castle': ('tile_effect_blinds7.png',
                       'tile_effect_blinds8.png',
                       'tile_effect_blinds9.png'),
            'Summon': ('tile_effect_blinds10.png',
                       'tile_effect_blinds11.png',
                       'tile_effect_blinds12.png'),
        }
    }

    # UI_SPRITE_DIRECTORY = os.path.join('assets', 'ui')
    CURSOR_SPRITE_DIRECTORY = os.path.join('assets', 'ui', 'cursors')
    CURSOR_SPRITE_FILES = {
        "default": "cursors1.png",
        "hover": "cursors2.png",
        "grab": "cursors3.png",
        "click": "cursors4.png",
        # "click2": "cursors5.png",
        # Sword?
        # Shield?
    }
    
    ICON_SPRITE_DIRECTORY = os.path.join('assets', 'ui', 'icons')
    ICON_SPRITE_FILES = {
        'ui': { # NOTE: ui icon tuples are (unclicked, clicked)
            'pause': ("ui_icons1.png", "ui_icons2.png"),
            'play': ("ui_icons3.png", "ui_icons4.png"),
            'undo': ("ui_icons5.png", "ui_icons6.png"),
            'settings': ("ui_icons7.png", "ui_icons8.png"),
        },
        'moodle': { # NOTE: moodle icon tuples are (white, black)
            # TODO: Subdict by loyalty?
            #       Best to avoid storing/loading one sprite multiple times.
            'check': ("Moodles1.png", "Moodles2.png"), # Swords
            # 'check': ("MoodlesSmall1.png", "MoodlesSmall2.png"), # Swords small
        }
    }
    
    def __init__(self):
        
        # TODO: Could lazily load some on first access?
        #       Unload sprites in some situations?
        
        # TODO: Shorten names.
        self.piece_sprites = self.load_sprites({}, self.PIECE_SPRITE_FILES, self.PIECE_SPRITE_DIRECTORY)
        # self.board_sprites = self.load_sprites({}, self.BOARD_SPRITE_FILES, self.BOARD_SPRITE_DIRECTORY)
        self.tile_sprites = self.load_sprites({}, self.TILE_SPRITE_FILES, self.TILE_SPRITE_DIRECTORY)
        self.tile_effect_sprites = self.load_sprites({}, self.TILE_EFFECT_SPRITE_FILES, self.TILE_EFFECT_SPRITE_DIRECTORY)
        self.cursor_sprites = self.load_sprites({}, self.CURSOR_SPRITE_FILES, self.CURSOR_SPRITE_DIRECTORY)
        self.icon_sprites = self.load_sprites({}, self.ICON_SPRITE_FILES, self.ICON_SPRITE_DIRECTORY)
        
        # TODO: DEPRECATE
        self.DEFAULT_PIECE_SPRITE = self.piece_sprites[Loyalty.NONE][PieceType.NONE]
        self.DEFAULT_TILE_SPRITE = self.tile_sprites[TileType.DEFAULT]
    
    @classmethod
    def load_sprites(cls, sprite_dict: dict, file_dict: dict, directory: str, verbose: bool=False) -> dict:
        """
        Recursively populate sprite_dict with image files from file_dict.
        """
        for key, value in file_dict.items():
            if isinstance(value, dict):
                # If the value is a dictionary, populate a sub dictionary in sprite_dict
                sprite_dict[key] = cls.load_sprites({}, value, directory)
            elif isinstance(value, tuple):
                sprite_dict[key] = tuple([cls.load_image(os.path.join(directory, k)) for k in value])
                if verbose:
                    for k in value: print(f"AssetLoader: Loaded {k} from {os.path.join(directory, key)}")
                
            elif isinstance(value, str):
                # If the value is a string, load the image and add it to sprite_dict
                sprite_dict[key] = cls.load_image(os.path.join(directory, value))
                if verbose: print(f"AssetLoader: Loaded {key} from {os.path.join(directory, value)}")
            else:
                raise ValueError(f"AssetLoader: Invalid value type: {type(value)}. Expected str or dict.")
        return sprite_dict

    @classmethod
    def load_image(cls, image_path: str, alpha:bool=True) -> pg.Surface:
        """
        Load a single sprite from a file.
        """
        img = pg.image.load(image_path)
        return img
        # TODO: Test whether this actually speeds up drawing?
        # if alpha:
        #     return img#.convert_alpha()
        # return img#.convert()

asset_loader = AssetLoader()
