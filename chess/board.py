import os
from pathlib import Path
import numpy as np
from typing import Optional, List, Union, Tuple, TypeAlias

from chess.tile import board_constructor, Tile

from chess.units.get_piece import get_piece_class
from chess.units.piece import ChessPiece

# from chess.units.pawn import Pawn
# from chess.units.bishop import Bishop
# from chess.units.rook import Rook
# from chess.units.knight import Knight
# from chess.units.queen import Queen
# from chess.units.king import King

from chess.chess_types import Piece, TileType, Position, Vector
from chess.chess_types import Loyalty, Direction
from chess.chess_types import Direction as D

# Chesstypes?
BoardTiles: TypeAlias = np.ndarray[Tile]

class Board:
    _board: BoardTiles
    
    move_history: List[Tuple[Position, Position]]
    turn_order: Tuple[Loyalty]
    turn: int
    
    selected_tile: Optional[Tile] # ? Have a 'game' manager to handle user interaction?
    
    # CSV file references (TODO: DEPRECATE)
    _initial_tiles: str
    _initial_pieces: str
    
    def __init__(self, tile_csv: str, piece_csv: str, turn_order: Tuple[Loyalty] = (Loyalty.WHITE, Loyalty.BLACK)):
        
        # TODO: Do not require csvs.
        #       Use dicts, and store as JSON.
        self._initial_tiles = tile_csv
        self._initial_pieces = piece_csv
        
        # Initialize board.
        self.load_state(tile_csv, piece_csv)
        
        # self.initial_board = self.board.copy() # Store initial piece positions? Or just rely on file...
        self.move_history: List[Tuple[Position, Position]] = []
        self.turn_order = turn_order
        self.turn = 0
        
        self.selected_tile: Optional[Tile] = None # Deprecate?
    
    @property
    def current_turn(self) -> Loyalty:
        """
        Returns the current turn.
        """
        return self.turn_order[self.turn % len(self.turn_order)]

    @property # Deprecate?
    def selected(self) -> Optional[ChessPiece]:
        return self.selected_tile.piece
    
    @property
    def shape(self) -> Tuple[int, int]: # NOTE: Reverse x and y for numpy.
        return self._board.shape[::-1]
    @property
    def width(self) -> int:
        return self.shape[0]
    @property
    def height(self) -> int:
        return self.shape[1]
    
    def __getitem__(self, pos: Position) -> Union[Tile, BoardTiles]:
        # Add 2nd dimension to 1D slices and indices.
        if isinstance(pos, slice): pos = (pos, slice(0, None))
        if isinstance(pos, int): pos = (pos, slice(0, None))
        return self._board[pos[1], pos[0]] # NOTE: Flip x and y for numpy.
        # return self.board[pos[::-1]]
        
    def at_pos(self, pos: Position) -> Tuple[Optional[Tile], Optional[ChessPiece]]:
        """
        Returns the tile and piece at the given position.
        """
        t = self.get_tile(pos)
        if t is None: return None, None
        return t, t.piece
    
    def get_tile(self, position: Position) -> Optional[Tile]:
        """
        Returns the tile at the given position.
        """
        if len(position) != 2:
            raise ValueError("Position must be a tuple of (x, y).")
        if 0 <= position[0] < self.width and 0 <= position[1] < self.height:
            return self[*position]
        return None
    
    
    # TODO: More complex state will be needed.
    #       One option is using 3+dimensional arrays.
    #           Each position having [tile, piece, loyalty, objects?]
    #       This still does not work great once pieces have more data (i.e. have pawns moved?).
    #       Also does not show whose turn it is.
    #       JSON will be better.
    def save_state(self, directory: Optional[str] = None) -> None:
        """
        Saves the current state of the board to a file.
        """
        if directory is None:
            # Get path to parent/saves
            directory = Path(__file__).parent / 'saves'
        
        filename1 = 'save{:%03d}_tiles.csv'
        filename2 = 'save{:%03d}_pieces.csv'
        i = 0
        while os.path.exists(directory / (filename1.format(i))) or os.path.exists(directory / (filename2.format(i))):
            i += 1
        filename1 = filename1.format(i)
        filename2 = filename2.format(i)
        
        tiles = np.zeros(self.shape, dtype=int)
        pieces = np.zeros(self.shape, dtype=int)
        for x, y in np.ndindex(self.shape):
            tiles[x, y] = self[x, y].tiletype.value
            pieces[x, y] = self[x, y].piece.piece_type.value if self[x, y].piece is not None else 0
        
        np.savetxt(filename1, tiles.T, fmt='%d', delimiter=',')
        np.savetxt(filename2, pieces.T, fmt='%d', delimiter=',')
        print(f"Saved board state to {filename1}_tiles.csv and {filename2}_pieces.csv")
        
    def load_state(self, board_csv: str, piece_csv: str):
    # def load_state(self, filename: Optional[str] = None, directory: Optional[str] = None):
        """
        Loads the state of the board from a file.
        """
        tiles = np.loadtxt(board_csv, dtype=int, delimiter=',').T
        pieces = np.loadtxt(piece_csv, dtype=int, delimiter=',').T
        
        self._board = board_constructor(tiles)
        
        for x, y in np.ndindex(pieces.shape):
            v = pieces[x, y]
            if v == 0: continue
            
            l = Loyalty.WHITE if v > 0 else Loyalty.BLACK
            
            # Select piece type based on value (TODO: Update to JSON)
            pc = get_piece_class(Piece(abs(v)))
            piece = pc(self, l, (x, y))
            
            # TODO: Do not place pieces on void?
            #       Have them die instantly? (TODO: Board.update?)
            self[x, y].piece = piece
            
        print(f"Loaded board state from {board_csv} and {piece_csv}") 

            
    # Implement iter to access tiles!
    # def __iter__(self):
    #     for x, y in np.ndindex(self.board.shape):
    #         yield self.board[y][x]
        # for y in range(self.height):
        #     for x in range(self.width):
        #         yield self.board[y][x]
    
