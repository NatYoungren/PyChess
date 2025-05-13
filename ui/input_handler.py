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
    
    def update_mousepos(self):
        """
        Update based on mouse position (hovered tile, dragged piece, etc).
        """
        # self.ui.m_pos = pg.mouse.get_pos()
        x, y = pg.mouse.get_pos() # TODO: Only use one get_pos per frame?
        bx, by = self.ui.board_origin
        bw, bh = self.ui.b_size

        if not (bx < x < bx+bw and by < y < by+bh):
            self.ui.h_tile = None
            return
        
        tx, ty = self.ui.tile_size
        _x, _y = (x - bx) // tx, (y - by) // ty
        
        tile = self.board.get_tile((_x, _y))
        self.ui.h_tile = tile # NOTE: Could be None
    
    def handle_event(self, event):
        """
        Handle user input events.
        """
        if event.type == pg.QUIT:
            self.running = False
            return
        
        if event.type == pg.KEYDOWN:
            self.handle_keydown(event)
            return
        
        if event.type == pg.MOUSEBUTTONDOWN:
            self.handle_click(event)
            return

        if event.type == pg.MOUSEMOTION:
            # self.
            return
        
    def handle_keydown(self, event):
        if event.key == pg.K_ESCAPE:
            self.running = False
            return
        
        if event.key == pg.K_SPACE:
            self.ui.hide_cursor = not self.ui.hide_cursor
            return

        # if event.key == pg.K_r:
        #     self.board.reset()
        #     return
        
        # if event.key == pg.K_s:
        #     self.board.save_state()
        #     return
        
        # if event.key == pg.K_l:
        #     self.board.load_state()
        #     return
        
    
    def handle_click(self, event):
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
            outcome = self.ui.s_piece.outcomes.get(tile, None)
            
            if self.board.realize(outcome):
                self.board.update()
                self.ui.s_tile = None
            else:
                if piece is not None and piece.loyalty == self.board.current_turn:
                    self.ui.s_tile = tile
