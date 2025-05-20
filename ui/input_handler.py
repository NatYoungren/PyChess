import pygame as pg
import numpy as np

from globalref import OBJREF

class InputHandler:
    """
    A class to handle user input for the chess game.
    """
    
    running: bool
    locked_board: bool
    
    def __init__(self):
        self.running = True
        
        self.locked_board = False
    
    def update_mousepos(self):
        """
        Update based on mouse position (hovered tile, dragged piece, etc).
        """
        if self.locked_board: return
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
    
    # TODO: Locked board could just be a class flag.
    def handle_event(self, event): 
        """
        Handle user input events.
        """
        match event.type:
            case pg.QUIT:
                self.running = False
        
            case pg.KEYDOWN:
                self.handle_keydown(event)
        
            case pg.MOUSEBUTTONDOWN:
                self.handle_click(event)

            case pg.MOUSEMOTION:
                pass
            
            case _:
                pass
                # print(f"DEBUG: INPUT_HANDLER.handle_event: Unknown event type: {event.type}")
        
    def handle_keydown(self, event):
        if event.key == pg.K_ESCAPE:
            self.running = False
            return

        if event.key == pg.K_SPACE:
            self.ui.hide_cursor = not self.ui.hide_cursor
            return

        if self.locked_board: return

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
        if self.locked_board: return
        
        bx, by = self.ui.board_origin
        bw, bh = self.ui.b_size

        x, y = pg.mouse.get_pos()
        if not (bx < x < bx+bw and by < y < by+bh):
            print("Clicked outside the board")
            return
        
        tx, ty = self.ui.tile_size
        _x, _y = (x - bx) // tx, (y - by) // ty
        
        tile, piece = self.board.at_pos((_x, _y))
        if event.button == 1: # Left click
            self.board_click(tile, piece)
        
        # TODO: Remove eventually.
        elif event.button == 3: # Right click
            print('DEBUG: INPUT_HANDLER.handle_click: Right click')
            tile.piece = None
            self.ui.s_tile = None
            self.ui.board.update()

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
                self.ui.s_tile = None
            else:
                if piece is not None and piece.loyalty == self.board.current_turn:
                    self.ui.s_tile = tile


    @property
    def ui(self):
        return OBJREF.UI
    
    @property
    def board(self):
        return self.ui.board
