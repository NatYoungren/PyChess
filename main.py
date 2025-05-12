import pygame as pg
import numpy as np
import os

from globalref import OBJREF#, board, surface


from chess.asset_loader import asset_loader as al

from chess.chess_types import Loyalty, PieceType
from chess.board import Board

board_csv = 'default_board.csv'
piece_csv = 'default_pieces.csv'


board_dir = 'chess/board_csvs'
piece_dir = 'chess/piece_csvs'
board_csv_path = os.path.join(board_dir, board_csv)
piece_csv_path = os.path.join(piece_dir, piece_csv)

board = Board(board_csv_path, piece_csv_path)
OBJREF.BOARD = board


from ui.chess_ui import ChessUI

ui = ChessUI.from_config()


# Define the background colour 
# using RGB color coding. 
background_colour = (234, 212, 252) 

tile_size = (64, 64)


# Create pg window
window_size = (board.width*tile_size[0], board.height*tile_size[1])
surface = pg.display.set_mode(window_size) 
OBJREF.SURFACE = surface

# Set the caption of the screen 
pg.display.set_caption('PyChess') 


def draw_board(surf, b, selected=None, viable=None):
    # TODO: Replace selected with tile / piece reference?
    if viable is None: viable = {}
    
    surf.fill(background_colour)
    for w, h in np.ndindex(board.shape):
        t = b[w, h]
        img = pg.transform.scale(t.sprite, (int(tile_size[0]), int(tile_size[0]))) # DO THIS WHEN LOADING SPRITE.
        surf.blit(img, (w*tile_size[0], h*tile_size[1]-(img.get_height()-tile_size[1])))
        
        # if (w+h)%2 == 0:
        #     pg.draw.rect(surf, (50, 50, 50), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))
            
        # else:
        #     pg.draw.rect(surf, (205, 205, 205), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))
    
    # Draw effect on selected tile.
    if selected is not None:
        w, h = selected.position
        rand_idx = np.random.randint(0, len(al.tile_effect_sprites['selected']))
        rand_rot = np.random.randint(0, 4)*90
        rand_flip = np.random.randint(0, 1, 2)
        
        img = al.tile_effect_sprites['selected'][rand_idx]
        img = pg.transform.rotate(img, rand_rot)
        img = pg.transform.flip(img, *rand_flip)
        img = pg.transform.scale(img, (int(tile_size[0]), int(tile_size[0])))
        surf.blit(img, (w*tile_size[0], h*tile_size[1]-(img.get_height()-tile_size[1])))
        # pg.draw.rect(surf, (50, 255, 50), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))

    # Draw effects on selectable tiles.
    for (w, h), oc in viable.items():
        # TODO: Just use name as key.
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
        rand_rot = np.random.randint(0, 4)*90
        rand_flip = np.random.randint(0, 1, 2)
        img = pg.transform.rotate(img, rand_rot)
        img = pg.transform.flip(img, *rand_flip)
        img = pg.transform.scale(img, (int(tile_size[0]), int(tile_size[0])))
        
        surf.blit(img, (w*tile_size[0], h*tile_size[1]-(img.get_height()-tile_size[1])))

        # pg.draw.rect(surf, (255, 50, 50), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))
        
    for w, h in np.ndindex(board.shape):
        t = b[w, h]
        p = t.piece
        if p != None:
            img = p.sprite
            ratio = img.get_height() / img.get_width()
            img = pg.transform.scale(img, (int(tile_size[0]), int(tile_size[0] * ratio)))
            surf.blit(img, (w*tile_size[0], h*tile_size[1]-(img.get_height()-tile_size[1])))
            
    pg.display.flip() 


draw_board(surface, board)

selected_tile = None
# selected_piece = None
# selected_square = None
viable_moves = None

# game loop
running = True
while running:
    
    for event in pg.event.get(): 
        
        # Check for QUIT event       
        if event.type == pg.QUIT: 
            running = False
            break
        
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            x = x // tile_size[0]
            y = y // tile_size[1]
            
            # Non-existent tile
            tile = board[x, y]
            if tile is None: continue
            piece = tile.piece
            
            if selected_tile is None:
                if piece is not None and piece.loyalty == board.current_turn:
                    # TODO: Indicate when a piece has no moves!
                    piece_moves = piece.options()
                    viable_moves = piece_moves
                    selected_tile = tile
                
            else:
                if viable_moves is not None:
                    outcome = viable_moves.get((x, y), None)
                    if outcome is not None:
                        outcome.realize((x, y))
                        board.move_history.append((selected_tile.position, (x, y)))
                        board.turn += 1
                    
                    selected_tile = None
                    viable_moves = None
                    
                
            draw_board(surface, board, selected_tile, viable_moves)
