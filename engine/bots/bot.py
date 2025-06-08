import numpy as np
from typing import Optional, Tuple, List, Dict

from utils.chess_types import Loyalty, PieceType, TileType
from chess.units.piece import ChessPiece

from globalref import GlobalAccessObject


# BOT TURN LOGIC:

# Inform that it is bots turn.
#   Update internal state/info.

# Until turn is over:
#   Select some outcome to play.
#   Wait for during preview.
#   Resolve that outcome.
#   Repeat.

# Inform GameManager that turn is over.


# TRANSPARENCY BOT LOGIC:
#   Select 1~4 possible pieces or outcomes.
#   Indicate them to the player.
#   Resolve one or more of them on bot turn.




class Bot(GlobalAccessObject):
    """
    Contains bot logic to prioritize and play moves.
    """

    loyalty: Loyalty
    
    # TODO: Store initial pieces?
    
    def __init__(self, loyalty: Loyalty):
        self.loyalty = loyalty
    
    @property
    def leaders(self) -> List[ChessPiece]:
        return self.board.loyal_leaders(self.loyalty)
    
    @property
    def pieces(self) -> List[ChessPiece]:
        return self.board.loyal_pieces(self.loyalty)
    
    @property
    def outcomes(self) -> Dict[ChessPiece, Dict[TileType, List[ChessPiece]]]:
        return {p: p.outcomes for p in self.pieces}
    
    def assert_turn(self):
        if self.board.current_turn != self.loyalty:
            raise ValueError(f"Bot {self.loyalty} cannot play on {self.board.current_turn} turn.")

    def play(self) -> Tuple[Optional[TileType], Optional[ChessPiece]]:
        raise NotImplementedError("This method should be implemented by subclasses.")
