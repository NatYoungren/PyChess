import os
import pygame as pg

from globalref import OBJREF


board_csv = 'default_board.csv'
# piece_csv = 'default_pieces.csv'

# board_csv = 'void_board.csv'
# piece_csv = 'void_pieces.csv'

# board_csv = 'obstacle_board.csv'
# piece_csv = 'obstacle_pieces.csv'

piece_csv = 'summoner_pieces.csv'

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

# Auto turn variables
auto_turn_timer = -1
auto_tile = None
auto_oc = None

while ih.running:

    # TODO: Need a game manager and bot classes.
    if not board.controlled_turn:
        if auto_turn_timer <= 0:
            auto_tile, auto_oc = board.random_outcome()
            if auto_oc is not None:
                ui.h_tile = auto_tile
                ui.s_piece = auto_oc.piece
                auto_turn_timer = 60
            else:
                auto_turn_timer = 0
        auto_turn_timer -= 1
        if auto_turn_timer <= 0:
            board.realize(auto_oc) if auto_oc is not None else board.next_turn()
            ui.s_tile = None
        
        
    ih.update_mousepos()
    for event in pg.event.get(): 
        ih.handle_event(event, locked_board=auto_turn_timer > 0)
    ui.draw()
    game_clock.tick(target_fps)

