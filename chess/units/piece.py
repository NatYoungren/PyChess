import numpy as np
from typing import List, Optional, Self, Dict, Tuple

from chess.chess_types import Position, Vector, Direction
from chess.chess_types import Loyalty, Piece
from chess.chess_types import DirCls as D

from chess.asset_loader import sprite_dict, DEFAULT_SPRITE

class ChessPiece:
    name: str
    
    board: object

    piece_type: Piece = Piece.NONE
    loyalty: Loyalty = Loyalty.NONE
    
    actions: List[object]
    
    sprite: object # TODO: Type
    facing: Direction # +0- X, +0- Y
    
    position: tuple[int, int]
    move_count: int
    
    # TODO: Can I avoid having the pieces store the board?
    #   Global reference instead?
    #   Or pass it in as needed?
    
    def __init__(self, board, loyalty: Loyalty=Loyalty.NONE, piece_type: Piece=Piece.NONE, position: Position = (0, 0), sprite=None):
        self.name = self.__class__.__name__

        self.board = board
        self.actions: List[object] = []
        
        self.loyalty: Loyalty = loyalty
        self.piece_type: Piece = piece_type
        
        if sprite is None:
            sprite = sprite_dict.get(self.loyalty, {}).get(self.piece_type, DEFAULT_SPRITE)
        self.sprite = sprite
        
        # TODO: Placeholder, deprecate / improve?
        self.facing = (0, -1) if loyalty == Loyalty.WHITE else (0, 1)
        self.facing = np.asarray(self.facing)
        
        self._position: Position = np.asarray(position) # TODO: Would this be good to store in piece?
        self.move_count: int = 0

        # Should track a turn-stamped history of positions?
        self.position_history: List[Position] = [self.position]
        self.move_history: List[Vector] = []
        # self.capture_history: List[Self] = []
    
    
    # # # # # # # # # #
    # TODO: Think this through and make it more elegant.
    def update_actions(self):
        """
        Update the actions for this piece.
        """
        for action in self.actions:
            action.update()
            
    def options(self): # Deprecate?
        self.update_actions()
        return self.get_options()
    
    def get_options(self) -> Dict[Position, object]: # Outcome!
        """
        Get the possible options for this piece.
        """
        options = {}
        for action in self.actions:
            # action.update()
            options.update(action.outcomes)
        return options
    #
    # # # # # # # # # #
    
    # def can_move(self):
    #     pass
    
    
    def move(self, position: Position):
        curr_tile = self.board[self.position]
        next_tile = self.board[position]
        if next_tile.piece is not None:
            self.capture(next_tile.piece)
        
        curr_tile.piece = None
        next_tile.piece = self
        self.moved_to(position)
    
    def moved_to(self, position: Position):
        vector = position - self.position
        
        self.position = position
        self.position_history.append(position)
        self.move_history.append(vector)
        
        self.move_count += 1

    
    def capture(self, piece: Self):
        # self.capture_history.append(piece)
        piece.captured(self)
    
    def captured(self, piece):
        self.board[self.position].piece = None
        # del self # TODO: What should happen?
    
    def get_line(self,
                 dir: Direction, length: int, start: Position=None,
                 can_move: bool = True,
                 enemy_ok: bool = True, ally_ok: bool = False,
                 jump_enemy: bool = False, jump_ally: bool = False,
                 jump_gap: bool = False,
                 ) -> List[Tuple[Position, Optional[object], Optional[Self]]]:
        """
        Get a line of (pos, tile, piece) tuples in the given direction.
        """
        line = []
        for i in range(1, length+1):
            v = dir * i
            pos, tile, piece = self.at_vec(v, start)
            
            if tile is None:
                if jump_gap:
                    continue
                else:
                    break
                
            piece = tile.piece
            if piece is not None: # If piece on tile
                if piece.loyalty == self.loyalty:
                    if ally_ok:
                        line.append((pos, tile, tile.piece))
                    if jump_ally:
                        continue
                    else:
                        break
                    
                else: # Enemy piece
                    if enemy_ok:
                        line.append((pos, tile, piece))
                    if jump_enemy:
                        continue
                    else:
                        break
                    
            else: # If no piece on tile
                if can_move:
                    line.append((pos, tile, None))
                else:
                    continue
        return line

    
    def at_vec(self, vector: Vector, start: Optional[Position]=None) -> Tuple[Position, Optional[object], Optional[Self]]:
        """
        Get the tile and piece at the given vector.
        """
        if start is None: start = self.position
        pos = start + self.orient_vector(vector)
        return pos, *self.board.at_pos(pos)
        # t = self.board.get_tile(pos)
        # if t is None: return None, None
        # return pos, t, t.piece
    
    # Input vector is relative to facing: [forward/backward, right/left]
    #   [+ is forward, + is right]
    # Output vector is in board coords: [x, y]
    def orient_vector(self, vector: Vector) -> Vector: # TODO: Matrix multiplication solution?
        return vector * self.facing[1] + vector[::-1] * self.facing[0]

    
    @property
    def position(self) -> Position:
        return np.array(self._position, dtype=int)
    
    @position.setter
    def position(self, value: Position):
        self._position = np.array(value, dtype=int)
    
    def __repr__(self):
        return f'{self.loyalty.name} {self.name}'