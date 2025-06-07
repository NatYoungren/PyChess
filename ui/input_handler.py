import pygame as pg
import numpy as np

from globalref import GlobalAccessObject

# # # # #
# DEBUG #
from utils.debug_utils import next_in_enum
from chess.tiles.get_tile import get_tile_class
from chess.units.get_piece import get_piece_class
from utils.chess_types import TileType, PieceType, Loyalty
# # # #


class InputHandler(GlobalAccessObject):
    """
    A class to handle user input for the chess game.
    """
    
    running: bool
    locked_board: bool
    
    def __init__(self):
        self.running = True
        self.locked_board = False
        
        # TODO: Store input state?
        self.m_pos = np.zeros(2, dtype=int) # Mouse position (for custom cursor)
    
    def update(self):
        """
        Update the input handler.
        """
        self.update_mousepos()
        for event in pg.event.get():
            self.handle_event(event)
    
    def update_mousepos(self):
        """
        Update based on mouse position (hovered tile, dragged piece, etc).
        """

        x, y = pg.mouse.get_pos()
        self.m_pos[:] = x, y # TODO: Only use one get_pos per frame?
        
        # Update UI hclickable.
        self.ui.update_hclickable((x, y)) # 
        # _ = self.ui.ui_get_hovered((x, y)) # Update hovered UI element, if any.
        
        if self.locked_board: return
        
        bx, by = self.ui.b_origin
        bw, bh = self.ui.b_size
        
        # If outside board, reset hovered tile.
        if not (bx < x < bx+bw and by < y < by+bh):
            self.ui.h_tile = None
            return
        
        tx, ty = self.ui.tile_size
        _x, _y = (x - bx) // tx, (y - by) // ty
        
        # NOTE: Update UI with hovered tile.
        tile = self.board.get_tile((_x, _y))
        self.ui.h_tile = tile # NOTE: Could be None
            
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
        
        x, y = event.pos
        bx, by = self.ui.b_origin
        bw, bh = self.ui.b_size

        # TODO: Handle UI interaction.
        if not (bx < x < bx+bw and by < y < by+bh):
            # print("Clicked outside the board")
            self.ui_click(event)
            return
        
        tx, ty = self.ui.tile_size
        _x, _y = (x - bx) // tx, (y - by) // ty
        
        tile, piece = self.board.at_pos((_x, _y))
        if event.button == 1: # Left click
            self.board_click(tile, piece)
        
        # # # # #
        # DEBUG #
        # TODO: Remove eventually.
        #
        # Change piece loyalty
        elif event.button == 3 and pg.key.get_mods() & pg.KMOD_CTRL and pg.key.get_mods() & pg.KMOD_SHIFT: # Ctrl + Shift + Right click
            print('DEBUG: INPUT_HANDLER.handle_click: Ctrl + Shift + Right click on tile:', _x, _y)
            if tile is None or piece is None:
                print('DEBUG: INPUT_HANDLER.handle_click: No tile or piece at position:', _x, _y)
                return
            new_loyalty = next_in_enum(piece.loyalty, Loyalty)
            new_piece = get_piece_class(piece.piece_type)(new_loyalty, tile.position)
            tile.piece = new_piece
            self.board.update()
        #
        # Change piece type
        elif event.button == 3 and pg.key.get_mods() & pg.KMOD_CTRL: # Ctrl + Right click
            print('DEBUG: INPUT_HANDLER.handle_click: Ctrl + Right click on tile:', _x, _y)
            if tile is None:
                print('DEBUG: INPUT_HANDLER.handle_click: No tile at position:', _x, _y)
                return
            if piece is None:
                next_piecetype = PieceType.NONE
                loyalty = Loyalty.WHITE
            else:
                next_piecetype = next_in_enum(piece.piece_type, PieceType)
                loyalty = piece.loyalty
            # print(piece, next_piecetype, loyalty)
            tile.piece = get_piece_class(next_piecetype)(loyalty, tile.position)
            self.board.update()
        #
        # Change tile type
        elif event.button == 3 and pg.key.get_mods() & pg.KMOD_SHIFT: # Shift + Right click
            print('DEBUG: INPUT_HANDLER.handle_click: Shift + Right click on tile:', _x, _y)
            if tile is None:
                next_tiletype = TileType.DEFAULT
            else:
                next_tiletype = next_in_enum(tile.tiletype, TileType)
            self.board[tile.position] = get_tile_class(next_tiletype)(tile.position)
            self.board[tile.position].piece = tile.piece
            tile.piece = None
            self.board.update() # NOTE: Kills pieces when toggling past deadly tiletypes.
        #
        # Remove piece
        elif event.button == 3: # Right click
            print('DEBUG: INPUT_HANDLER.handle_click: Right click on tile:', _x, _y)
            tile.piece = None
            self.ui.s_tile = None
            self.board.update()
        # # # # #


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

    def ui_click(self, event: pg.event.Event):
        # print('HANDLING UI CLICK')
        self.ui.ui_click(event.pos) # TODO: Add m1, m2 parameters
