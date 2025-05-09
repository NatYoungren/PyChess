import os
import pygame 
from chess.board_OLD import Board
import numpy as np

# Define the background colour 
# using RGB color coding. 
background_colour = (234, 212, 252) 
  
tile_size = (64, 64)


# Define the dimensions of 
# screen object(width,height) 
screen = pygame.display.set_mode((800, 800)) 


# Set the caption of the screen 
pygame.display.set_caption('PyChess') 


    # pygame.transform.scale(sprite_dict[key], (int(100), int(100)))


# sprite_dict = {
#     1: pygame.image.load("imgs/wPawn.png"),
#     2: pygame.image.load("imgs/wKnight.png"),
#     3: pygame.image.load("imgs/wBishop.png"),
#     4: pygame.image.load("imgs/wRook.png"),
#     5: pygame.image.load("imgs/wQueen.png"),
#     6: pygame.image.load("imgs/wKing.png"),
#     -1: pygame.image.load("imgs/bPawn.png"),
#     -2: pygame.image.load("imgs/bKnight.png"),
#     -3: pygame.image.load("imgs/bBishop.png"),
#     -4: pygame.image.load("imgs/bRook.png"),
#     -5: pygame.image.load("imgs/bQueen.png"),
#     -6: pygame.image.load("imgs/bKing.png")
# }


board = Board()
running = True



def draw_board(surf, b, s=None, v=None):
    surf.fill(background_colour) 
    for w in range(b.shape[0]):
        for h in range(b.shape[1]):
            if s is not None and (w, h) == s:
                pygame.draw.rect(surf, (50, 255, 50), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))

            elif v is not None and v[w, h] == 1:
                pygame.draw.rect(surf, (255, 50, 50), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))

            elif (w+h)%2 == 0:
                pygame.draw.rect(surf, (50, 50, 50), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))
                
            else:
                pygame.draw.rect(surf, (205, 205, 205), (w*tile_size[0], h*tile_size[1], tile_size[0], tile_size[1]))

    for w in range(b.shape[0]):
        for h in range(b.shape[1]):
            if b.board[w, h] != 0:
                img = sprite_dict[b.board[w, h]]
                ratio = img.get_height() / img.get_width()
                print(ratio)
                img = pygame.transform.scale(img, (int(tile_size[0]), int(tile_size[0] * ratio)))

                surf.blit(img, (w*tile_size[0], h*tile_size[1]-(img.get_height()-tile_size[1])))
            
    pygame.display.flip() 


draw_board(screen, board)


current_turn = 1
selected_square = None
viable_moves = None

# game loop 
while running: 
    
    for event in pygame.event.get(): 
        
        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            running = False
            break
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = x // tile_size[0]
            y = y // tile_size[1]
            if x < 0 or x >= board.shape[0] or y < 0 or y >= board.shape[1]:
                continue

            if selected_square is None:
                if np.sign(board.board[x, y]) == current_turn:
                    selected_square = (x, y)
                    viable_moves = board.viable_moves(selected_square)
                    # print('selected', selected_square)
                
            else:
                if viable_moves is not None and viable_moves[x, y] == 1:
                    board.board[x, y] = board.board[selected_square]
                    board.board[selected_square] = 0
                    current_turn = -current_turn
                selected_square = None
                viable_moves = None
                
            draw_board(screen, board, selected_square, viable_moves)
