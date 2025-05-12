import pygame as pg
import numpy as np

class InputHandler:
    """
    A class to handle user input for the chess game.
    """
    def __init__(self, ui):
        self.ui = ui
        # self.selected_tile = None
        # self.selected_piece = None
        # self.selected_square = None
        # self.viable_moves = None
        self.running = True
    
    @property
    def board(self):
        return self.ui.board
    
    def handle_event(self, event):
        """
        Handle user input events.
        """
        if event.type == pg.QUIT:
            self.running = False
            return
        
        if event.type == pg.MOUSEBUTTONDOWN:
            bx, by = self.ui.board_origin
            bw, bh = self.ui.b_size

            x, y = pg.mouse.get_pos()
            if not (bx < x < bx+bw or by < y < by+bh):
                print("Clicked outside the board")
                return
            
            tx, ty = self.ui.tile_size
            _x, _y = (x - bx) // tx, (y - by) // ty
            
            tile, piece = self.board.at_pos((_x, _y))
            self.board_click(tile, piece)

            # if tile is None: return # Non-existent tile
            # piece = tile.piece
            
            # if self.board.selected_tile is None:
            #     if piece is not None and piece.loyalty == self.board.current_turn:
            #         pass
    
    def board_click(self, tile=None, piece=None):
        """
        Handle a click on the board.
        """
        # Deselect if no tile clicked.
        if tile is None:# or piece is None:
            self.board.selected_tile = None
            return
        
        if self.board.selected_tile is None:
            if piece is not None and piece.loyalty == self.board.current_turn:
                piece.options() # This should be done each turn!
                self.board.selected_tile = tile
                
        else:
            selected_piece = self.board.selected
            if selected_piece is not None:
                outcome = selected_piece.get_options().get(tile.position, None)
                if outcome is not None:
                    outcome.realize(tile.position)
                    self.board.move_history.append((tile.position, selected_piece.position))
                    self.board.turn += 1
                    self.board.selected_tile = None
                else:
                    if piece is not None and piece.loyalty == self.board.current_turn:
                        self.board.selected_tile = tile
                        piece.options()
