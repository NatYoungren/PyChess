import pygame as pg
import numpy as np
import os

from chess.chess_types import Loyalty, Piece

from chess.board import Board

board_csv = 'default_board.csv'
piece_csv = 'default_pieces.csv'


board_dir = 'chess/board_csvs'
piece_dir = 'chess/piece_csvs'
board_csv_path = os.path.join(board_dir, board_csv)
piece_csv_path = os.path.join(piece_dir, piece_csv)

board = Board(board_csv_path, piece_csv_path)



# Define the background colour 
# using RGB color coding. 
background_colour = (234, 212, 252) 
  
tile_size = (64, 64)


# Create pg window
window_size = (board.width*tile_size[0], board.height*tile_size[1])
screen = pg.display.set_mode(window_size) 


# Set the caption of the screen 
pg.display.set_caption('PyChess') 


def draw_board(surf, b, selected=None, viable=None):
    surf.fill(background_colour) 
    for w, h in np.ndindex(board.shape):
        if (w+h)%2 == 0:
            pg.draw.rect(surf, (50, 50, 50), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))
            
        else:
            pg.draw.rect(surf, (205, 205, 205), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))
    
    if selected is not None:
        w, h = selected.position
        pg.draw.rect(surf, (50, 255, 50), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))

    if viable is not None:
        for (w, h) in viable:
            pg.draw.rect(surf, (255, 50, 50), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))

    for w, h in np.ndindex(board.shape):
        t = b[w, h]
        p = t.piece
        if p != None:
            img = p.sprite
            # img = sprite_dict[b.board[w, h]]
            ratio = img.get_height() / img.get_width()
            img = pg.transform.scale(img, (int(tile_size[0]), int(tile_size[0] * ratio)))

            surf.blit(img, (w*tile_size[0], h*tile_size[1]-(img.get_height()-tile_size[1])))
            
    pg.display.flip() 


draw_board(screen, board)

# turn_order = [Loyalty.WHITE, Loyalty.BLACK]
# current_turn = 0

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
                    # print('selected', selected_tile)
                    # selected_piece = piece
                    # viable_moves = piece.viable_moves#board.viable_moves(selected_tile)
                    
                # if np.sign(board.board[x, y]) == current_turn:
                #     selected_square = (x, y)
                #     viable_moves = board.viable_moves(selected_square)
                    # print('selected', selected_square)
                
            else:
                # if viable_moves is not None and viable_moves[x, y] == 1:
                if viable_moves is not None and any(x == move[0] and y == move[1] for move in viable_moves):
                    # selected_tile.move((x, y))
                    # TODO: USE BOARD MOVE FUNCTION.
                    
                    selected_tile.piece.move((x, y))
                    # board[x, y] = board[selected_square]
                    # board[selected_square] = 0
                    
                    board.move_history.append((selected_tile.position, (x, y)))
                    board.turn += 1
                    
                selected_tile = None
                viable_moves = None
                
            draw_board(screen, board, selected_tile, viable_moves)
