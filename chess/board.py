import numpy as np
from typing import Optional, List, Union, Tuple, TypeAlias, Dict

from globalref import GlobalAccessObject

from chess.tiles.get_tile import get_tile_class
from chess.tiles.tile import Tile

from chess.units.get_piece import get_piece_class
from chess.units.piece import ChessPiece

from utils.chess_types import PieceType, TileType, Position, Vector
from utils.chess_types import Loyalty, Direction
from utils.chess_types import Direction as D

from utils.game_utils import write_json, read_state_json # DEBUG

from chess.actions.outcome import Outcome

# Chesstypes?
BoardTiles: TypeAlias = np.ndarray[Tile]

class Board(GlobalAccessObject):
    # Board Tiles (contains Pieces)
    _board: BoardTiles
    
    # Game data
    move_history: List[Tuple[Position, Position]]
    turn_order: List[Loyalty]
    turn: int # Number of turns taken OR skipped.
    # TODO: Need 'round number' to track cycles of turns.
    
    # CSV file references (TODO: DEPRECATE)
    _initial_tiles: str
    _initial_pieces: str
    
    _checks: List[Tuple[ChessPiece, ChessPiece, Outcome]] # Checkee, checker, outcome
    
    controlled_factions: Tuple[Loyalty, ...]
    turn_order: List[Loyalty]
    
    # Leadership points per faction.
    MAX_LEADERSHIP: int = 5
    leadership_pts: Dict[Loyalty, int]
    
    # Stored states of board and pieces.
    #   Index = turn number?
    #   None = no state, Dict = state for that turn.
    
    # State contents: # TODO: JSON compatible.
    #   tiles: (TileType, Tile data) # TODO: Use a dataclass?
    #   pieces: (PieceType, Piece data) # TODO: Use a dataclass?
    #   current_turn: Loyalty
    #   ~ turn order:  List[Loyalty, ...]?
    #   ~ turn: int
    #   leadership_pts: Dict[Loyalty, int]
    #   
    state_cache: List[Optional[Dict]]
    
    def __init__(self,
                 state_json: Union[str, Dict],
                 controlled_factions: Tuple[Loyalty, ...] = (Loyalty.WHITE,),
                 turn_order: Optional[List[Loyalty]] = None):
        
        state_data = state_json if isinstance(state_json, dict) else read_state_json(state_json)
        if turn_order is not None: state_data['turn_order'] = [l.value for l in turn_order]
        self.load_state(state_data)  # Load initial state from JSON
        
        # self.initial_board = self.board.copy() # Store initial piece positions? Or just rely on file...
        self.move_history: List[Tuple[Position, Position]] = [] # Deprecate?
        # self.faction_history: Dict[Loyalty, List[Tuple[int, ChessPiece]]] = {l: [] for l in Loyalty} # Deprecate?
        self.history: List[Outcome] = [] # NOTE: List[Optional[Outcome]] now?
        
        self._checks = []
        
        self.controlled_factions = controlled_factions
        # if turn_order is None:
            # turn_order = [value for value in Loyalty]
        # self.turn_order = turn_order
        # self.turn = 0
        
        # self.leadership_pts = {l: 3 for l in Loyalty}
        
        self.state_cache: List[Dict] = []
        # self.cache_state()  # Cache initial state?
    
    
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
    
    def get_leadership(self, loyalty: Optional[Loyalty] = None) -> int:
        """
        Returns the leadership points of the given faction (defaults to current faction).
        """
        if loyalty is None: loyalty = self.current_turn
        return self.leadership_pts.get(loyalty, 0)
    
    def update_leadership(self, delta: int, loyalty: Optional[Loyalty] = None) -> None:
        """
        Updates the leadership points of the given faction.
        """
        if loyalty is None: loyalty = self.current_turn
        if loyalty not in self.leadership_pts:
            raise ValueError(f"Loyalty {loyalty} not found in leadership points.")
        self.leadership_pts[loyalty] = max(0, min(self.MAX_LEADERSHIP, self.leadership_pts[loyalty] + delta))
    
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
    def update(self, turn_changed: bool = False) -> None:
        """
        Updates all pieces and board.  
        Called at start of each turn.
        """
        for tile in self:
            tile.update()
            
            if tile.piece is not None:
                if turn_changed: tile.piece.turn_changed()
                tile.piece.update()
        
        self._checks = self.get_checks() # TODO: Give outcomes a 'checking' flag which they can set?
    
    def realize(self, outcome: Optional[Outcome]) -> bool:
        """
        Realizes the outcome of an action.
        """
        # self.selected_tile = None
        if outcome is None: return False
        outcome.realize() # TODO: Have Outcomes store turn when generated?
        self.history.append(outcome)
        self.next_turn()
        return True
    
    def next_turn(self, loop_to: Optional[Loyalty]=None) -> None:
        """
        Moves to the next turn.
        """
        if loop_to is None: loop_to = self.current_turn
        self.turn += 1
        self.update(turn_changed=True)
        
        # Infinite loop prevention turn skipping.
        if loop_to != self.current_turn: # TODO: This is hacky, improve.    
            # Skip turns
            lp = self.loyal_pieces()
            lpoc = [True if p.outcomes else False for p in lp]
            if not lp or not any(lpoc):
                return self.next_turn(loop_to=loop_to)
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
        if isinstance(pos, (slice, int, np.int64)): pos = (pos, slice(0, None))
        return self._board[pos[1], pos[0]] # NOTE: Flip x and y for numpy.
        # return self.board[pos[::-1]]
    
    # TODO: Validate setitem with slices.
    def __setitem__(self, pos: Position, value: Tile) -> None:
        # Add 2nd dimension to 1D slices and indices.
        if isinstance(pos, (slice, int, np.int64)): pos = (pos, slice(0, None))
        self._board[pos[1], pos[0]] = value
    
    
    def clear_cache(self) -> None:
        self.state_cache.clear()
    
    def get_state(self) -> Dict:
        """
        Generates a state dictionary of the current board and pieces.
        """
        state = {
                'tiles': np.array([[tile.tiletype.value for tile in row] for row in self._board]).T,
                'pieces': np.array([[tile.piece.piece_type.value if tile.piece else 0 for tile in row] for row in self._board]).T,
                'piece_loyalties': np.array([[tile.piece.loyalty.value if tile.piece else 0 for tile in row] for row in self._board]).T,
                # 'current_turn': self.current_turn.value,
                'turn_order': [l.value for l in self.turn_order],
                'turn': self.turn,
                'leadership_pts': {l.value: pts for l, pts in self.leadership_pts.items()}
            }
        return state
    
    # def cache_state(self, state_layer: int = 0) -> int:
    def cache_state(self, idx: Optional[int]=None, save_json_DEBUG: bool = False) -> int:
        """
        Caches the current state of the board and pieces.
        Returns the index of the cached state.
        """
        
        if idx is None:
            idx = len(self.state_cache)
        
        # Ensure cache is large enough
        while len(self.state_cache) <= idx: # TODO: Is this dumb?
            self.state_cache.append(None)
        
        self.state_cache[idx] = self.get_state()    # Insert current state
        # self.state_cache = self.state_cache[:idx + 1]  # Trim cache to current index
        
        # DEBUG
        if save_json_DEBUG:
            # Save state to JSON file
            write_json(f'state_cache/state_{idx}.json', self.state_cache[idx])  # Save state to JSON file
            print(f"DEBUG: Saved file state_cache/state_{idx}.json")
        # DEBUG
        
        return idx
    
    def uncache_state(self, idx: int) -> Optional[Dict]:
        """
        Uncaches the state at the given index.
        Returns the state or None if index is out of bounds.
        """
        if idx < 0 or idx >= len(self.state_cache):
            print(f"Uncache state: Index {idx} out of bounds.")
            return None
        return self.state_cache[idx]
    
    def load_cached_state(self, idx: int) -> bool:
        """
        Loads the cached state at the given index.
        """
        state = self.uncache_state(idx)
        if state is None:
            print(f"Load cached state: No state found at index {idx}.")
            return False
        
        self.load_state(state)
        self.update()
        return True
    
    def load_state(self, state: Dict):
        # Load tiles
        self._board = board_constructor(state['tiles'])
        self.turn = state['turn']
        self.turn_order = [Loyalty(l) for l in state['turn_order']]
        self.leadership_pts = {Loyalty(l): pts for l, pts in state['leadership_pts'].items()}
        
        pieces = state['pieces']
        piece_loyalties = state['piece_loyalties']
        # Load pieces
        for x, y in np.ndindex(self.shape):
            v = pieces[x, y]
            if v == 0: continue
            
            l = Loyalty(piece_loyalties[x, y])
            
            # Select piece type based on value
            pc = get_piece_class(PieceType(abs(v)))
            piece = pc(loyalty=l, position=(x, y))
            self[x, y].piece = piece
        
        return True

# TODO: Classmethod?
#       Add a piece constructor?
def board_constructor(tile_array: List[List[TileType]]) -> BoardTiles:
    """
    Constructs a board from a 2D array of TileType.
    """
    height = len(tile_array)
    width = len(tile_array[0])
    
    board_tiles = np.zeros((height, width), dtype=object)
    
    for x in range(height):
        for y in range(width):
            tiletype = tile_array[x][y]
            tc = get_tile_class(TileType(tiletype))
            board_tiles[y][x] = tc((x, y))
    
    return board_tiles#.T if transpose else board_tiles