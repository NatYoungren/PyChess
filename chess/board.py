import os
from pathlib import Path
import numpy as np
from typing import Optional, List, Union, Tuple, TypeAlias

from globalref import GlobalAccessObject

from chess.tiles.get_tile import get_tile_class
from chess.tiles.tile import Tile

from chess.units.get_piece import get_piece_class
from chess.units.piece import ChessPiece

# from chess.units.pawn import Pawn
# from chess.units.bishop import Bishop
# from chess.units.rook import Rook
# from chess.units.knight import Knight
# from chess.units.queen import Queen
# from chess.units.king import King

from chess.chess_types import PieceType, TileType, Position, Vector
from chess.chess_types import Loyalty, Direction
from chess.chess_types import Direction as D

from chess.actions.outcome import Outcome

# Chesstypes?
BoardTiles: TypeAlias = np.ndarray[Tile]

class Board(GlobalAccessObject):
    # Board Tiles (contains Pieces)
    _board: BoardTiles
    
    # Game data
    move_history: List[Tuple[Position, Position]]
    turn_order: List[Loyalty]
    turn: int
        
    # CSV file references (TODO: DEPRECATE)
    _initial_tiles: str
    _initial_pieces: str
    
    # Checkee, checker, outcome
    _checks: List[Tuple[ChessPiece, ChessPiece, Outcome]] = []
    
    def __init__(self, tile_csv: str, piece_csv: str,
                 controlled_factions: Tuple[Loyalty, ...] = (Loyalty.WHITE,),
                 turn_order: Optional[List[Loyalty]] = None):
        
        # TODO: Do not require csvs.
        #       Use dicts, and store as JSON.
        self._initial_tiles = tile_csv
        self._initial_pieces = piece_csv
        
        # Initialize board.
        self.load_state(tile_csv, piece_csv)
        
        # self.initial_board = self.board.copy() # Store initial piece positions? Or just rely on file...
        self.move_history: List[Tuple[Position, Position]] = [] # Deprecate?
        self.history: List[Outcome] = [] # NOTE: List[Optional[Outcome]] now?
        
        self.controlled_factions = controlled_factions
        if turn_order is None:
            turn_order = [value for value in Loyalty]
        self.turn_order = turn_order
        self.turn = 0
        
    # # #
    # TEMPORARY - AI TURN LOGIC
    # TODO: This is a placeholder for future bot logic.
    def random_outcome(self, loyalty: Optional[Loyalty] = None) -> Tuple[Optional[Tile], Optional[Outcome]]:
        """
        Returns a random outcome for the given loyalty.
        """        
        # Get all pieces for the given loyalty.
        pieces = self.loyal_pieces(loyalty)
        np.random.shuffle(pieces)
        for p in pieces:
            if p.outcomes:
                oc_t = np.random.choice(list(p.outcomes.keys()))
                oc = p.outcomes[oc_t]
                return oc_t, oc
            # for oc in np.random.shuffle(list(p.outcomes.values())):
            #     return oc
        return None, None       
    # # #
    
    # # #
    # Getters
    def loyal_pieces(self, loyalty: Optional[Loyalty] = None) -> List[ChessPiece]:
        """
        Returns all pieces from the given faction (defaults to current faction).
        """
        if loyalty is None: loyalty = self.current_turn
        # return [t.piece for t in self if (t.piece is not None and t.piece.loyalty == loyalty)]
        return [p for p in self.pieces if p.loyalty == loyalty]
    
    def disloyal_pieces(self, loyalty: Optional[Loyalty] = None) -> List[ChessPiece]:
        """
        Returns all pieces not from to given faction (defaults to current faction).
        """
        if loyalty is None: loyalty = self.current_turn
        return [p for p in self.pieces if p.loyalty != loyalty]
    
    def loyal_leaders(self, loyalty: Optional[Loyalty] = None) -> List[ChessPiece]:
        return [p for p in self.loyal_pieces(loyalty) if p.is_leader]
    
    def get_checks(self, loyalty: Optional[Loyalty] = None) -> List[Tuple[ChessPiece, ChessPiece, Outcome]]:
        checks = []
        ll = self.loyal_leaders(loyalty)
        for p in self.disloyal_pieces(loyalty):
            for l in ll:
                # TODO: This could be made much more accurate.
                check_oc = p.outcomes.get(self[l.position], None)
                if check_oc is not None and check_oc.name == 'Capture': # and isinstance(check_oc, Capture):
                    checks.append((l, p, check_oc))
                    # TODO: Add an effect or highlight to show checking pieces?
                    #       A preview system which has backtracking is becoming more necessary
        return checks
                    
    
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
    # # #
    
    
    # # #
    # Turn logic
    def update(self) -> None:
        """
        Updates all pieces and board.  
        Called at start of each turn
        """
        for tile in self:
            tile.update()
            if tile.piece is not None:
                tile.piece.update()

    def realize(self, outcome: Optional[Outcome]) -> bool:
        """
        Realizes the outcome of an action.
        """
        # self.selected_tile = None
        if outcome is None: return False
        outcome.realize(self) # TODO: Have Outcomes store turn when generated?
        self.history.append(outcome)
        self.next_turn()
        return True
    
    def next_turn(self, loop_to: Optional[Loyalty]=None) -> None:
        """
        Moves to the next turn.
        """
        if loop_to is None: loop_to = self.current_turn
        self.turn += 1
        self.update()
        
        # Infinite loop prevention turn skipping.
        if loop_to != self.current_turn: # TODO: This is hacky, improve.    
            # Skip turns
            lp = self.loyal_pieces()
            lpoc = [True if p.outcomes else False for p in lp]
            if not lp or not any(lpoc):
                self.next_turn(loop_to=loop_to)
        
        # TODO: Move to update?
        #       Give outcomes a 'checking' flag which they can set?
        self._checks = self.get_checks()
    # # #
    
    
    # # #
    # Properties
    @property
    def current_turn(self) -> Loyalty:
        return self.turn_order[self.turn % len(self.turn_order)]
    
    @property
    def controlled_turn(self) -> bool:
        """
        Returns True if current turn is controlled by player.
        """
        return self.current_turn in self.controlled_factions
    
    @property
    def pieces(self):
        """
        Returns all pieces on the board.
        """
        return [t.piece for t in self if t.piece is not None]
    
    @property
    def shape(self) -> Tuple[int, int]: # NOTE: Reverse x and y for numpy.
        return self._board.shape[::-1]
    
    @property
    def width(self) -> int:
        return self.shape[0]
    
    @property
    def height(self) -> int:
        return self.shape[1]
    # # #
    
    def __iter__(self):
        for x, y in np.ndindex(self.shape):
            yield self[x, y]
    
    def __getitem__(self, pos: Position) -> Union[Tile, BoardTiles]:
        # Add 2nd dimension to 1D slices and indices.
        if isinstance(pos, slice): pos = (pos, slice(0, None))
        if isinstance(pos, int): pos = (pos, slice(0, None))
        return self._board[pos[1], pos[0]] # NOTE: Flip x and y for numpy.
        # return self.board[pos[::-1]]
    
    
    # TODO: More complex state will be needed.
    #       One option is using 3+dimensional arrays.
    #           Each position having [tile, piece, loyalty, objects?]
    #       This still does not work great once pieces have more data (i.e. have pawns moved?).
    #       Also does not show whose turn it is.
    #       JSON will be better.
    def save_state(self, directory: Optional[str] = None) -> None:
        """
        Saves current tiles and pieces to CSV files.
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
        Loads tiles and pieecs from CSV files.
        """
        tiles = np.loadtxt(board_csv, dtype=int, delimiter=',').T
        pieces = np.loadtxt(piece_csv, dtype=int, delimiter=',').T
        
        self._board = board_constructor(tiles)
        
        for x, y in np.ndindex(pieces.shape):
            v = pieces[x, y]
            if v == 0: continue
            
            l = Loyalty.WHITE if v > 0 else Loyalty.BLACK
            
            # Select piece type based on value (TODO: Update to JSON)
            pc = get_piece_class(PieceType(abs(v)))
            piece = pc(loyalty=l, position=(x, y))
            
            # TODO: Do not place pieces on void?
            #       Have them die instantly? (TODO: Board.update?)
            self[x, y].piece = piece
            
        print(f"Loaded board state from {board_csv} and {piece_csv}") 


# TODO: Classmethod?
#       Add a piece constructor?
def board_constructor(tile_array: List[List[TileType]]) -> BoardTiles:
    """
    Constructs a board from a 2D array of TileType.
    """
    height = len(tile_array)
    width = len(tile_array[0])
    
    board_tiles = np.zeros((height, width), dtype=object)
    
    for y in range(height):
        for x in range(width):
            tiletype = tile_array[x][y]
            tc = get_tile_class(TileType(tiletype))
            board_tiles[y][x] = tc((x, y))
    
    return board_tiles