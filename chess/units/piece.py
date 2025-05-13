import numpy as np
from typing import List, Optional, Self, Dict, Tuple

from chess.chess_types import Position, Vector, Direction
from chess.chess_types import Loyalty, PieceType
from chess.chess_types import DirCls as D

from chess.asset_loader import asset_loader as al

from globalref import OBJREF


class ChessPiece:
    name: str

    piece_type: PieceType = PieceType.NONE
    loyalty: Loyalty = Loyalty.NONE
    
    actions: List[object]
    
    sprite: object # TODO: Type
    facing: Direction # +0- X, +0- Y
    
    _position: tuple[int, int]
    move_count: int
    
    # TODO: Can I avoid having the pieces store the board?
    #       Global reference instead?
    #       Or pass it in as needed?
    
    def __init__(self,
                 loyalty: Loyalty=Loyalty.NONE,
                 piece_type: PieceType=PieceType.NONE,
                 position: Position = (0, 0)):
        self.name = self.__class__.__name__

        self.actions: List[object] = []
        
        self.loyalty: Loyalty = loyalty
        self.piece_type: PieceType = piece_type
        
        self.sprite = al.piece_sprites.get(self.loyalty, {}).get(self.piece_type, al.DEFAULT_PIECE_SPRITE)
        
        # TODO: Placeholder, deprecate / improve?
        self.facing = (0, -1) if loyalty == Loyalty.WHITE else (0, 1)
        self.facing = np.asarray(self.facing)
        
        self._position: Position = np.asarray(position) # TODO: Would this be good to store in piece?
        self.move_count: int = 0

        # Should track a turn-stamped history of positions?
        self.position_history: List[Position] = [self.position]
        self.move_history: List[Vector] = []
        
        # Tile -> Outcome
        self._outcomes: Optional[Dict[object, object]] = None # TODO: Use a better type?
    
    # # # # # # # # # #
    # ACTION METHODS
    def update(self):
        """
        Update all actions for this piece.
        """
        self._outcomes = None # Delete cached outcomes?
        for action in self.actions:
            action.update()

    # returns: Tile -> Outcome
    @property
    def outcomes(self) -> Dict[object, object]:
        """
        Returns possible action outcomes for this piece.
        """
        if self._outcomes is None:
            self._outcomes = {}
            for action in self.actions:
                self._outcomes.update(action.outcomes)
                
        return self._outcomes
    #
    # # # # # # # # # #
    
    # def can_move(self):
    #     pass
    
    # Put these methods in board?
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
    
    # # #
    # HELPER METHODS
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
    
    def orient_vector(self, vector: Vector) -> Vector: # TODO: Matrix multiplication solution?
        # Input vector is relative to facing: [forward/backward, right/left]
        #   [+ is forward, + is right]
        # Output vector is in board coords: [x, y]
        return vector * self.facing[1] + vector[::-1] * self.facing[0]
    #
    # # #
    
    
    @property
    def position(self) -> Position:
        return np.array(self._position, dtype=int)
    
    @position.setter
    def position(self, value: Position):
        self._position = np.array(value, dtype=int)
    
    @property
    def board(self) -> object:
        return OBJREF.BOARD
    
    def __repr__(self):
        return f'{self.loyalty.name} {self.name}'