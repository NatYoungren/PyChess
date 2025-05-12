import pygame as pg
import numpy as np

class InputHandler:
    """
    A class to handle user input for the chess game.
    """
    def __init__(self, ui):
        self.ui = ui
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
            if not (bx < x < bx+bw and by < y < by+bh):
                print("Clicked outside the board")
                return
            
            tx, ty = self.ui.tile_size
            _x, _y = (x - bx) // tx, (y - by) // ty
            
            tile, piece = self.board.at_pos((_x, _y))
            self.board_click(tile, piece)
    
    def board_click(self, tile=None, piece=None):
        """
        Handle a click on the board.
        """
        # Deselect if no tile clicked.
        if tile is None:
            self.ui.s_tile = None
            return
        
        if self.ui.s_tile is None:
            if piece is not None and piece.loyalty == self.board.current_turn:
                self.ui.s_tile = tile
                
            else: # Clicked on empty tile or enemy piece
                self.ui.s_tile = None
            return
        
        if self.ui.s_piece is not None:
            outcome = self.ui.s_piece.outcomes().get(tile, None)
            
            if self.board.realize(outcome):
                self.board.update()
                self.ui.s_tile = None
            else:
                if piece is not None and piece.loyalty == self.board.current_turn:
                    self.ui.s_tile = tile
