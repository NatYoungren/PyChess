import os
import pygame as pg

from globalref import OBJREF


# board_csv = 'default_board.csv'
# piece_csv = 'default_pieces.csv'

# board_csv = 'void_board.csv'
# piece_csv = 'void_pieces.csv'

board_csv = 'obstacle_board.csv'
piece_csv = 'obstacle_pieces.csv'

board_dir = 'chess/board_csvs'
piece_dir = 'chess/piece_csvs'
board_csv_path = os.path.join(board_dir, board_csv)
piece_csv_path = os.path.join(piece_dir, piece_csv)


from chess.board import Board
board = Board(board_csv_path, piece_csv_path)
OBJREF.BOARD = board


from ui.chess_ui import ChessUI
ui = ChessUI.from_config()
OBJREF.UI = ui


from ui.input_handler import InputHandler
ih = InputHandler(ui)

board.update()


# game loop
target_fps = 60
game_clock = pg.time.Clock()
while ih.running:
    ih.update_mousepos()
    for event in pg.event.get(): 
        ih.handle_event(event)
    ui.draw()
    game_clock.tick(target_fps)

