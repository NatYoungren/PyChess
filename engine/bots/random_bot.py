import numpy as np
from typing import Optional, Tuple, List, Dict

from engine.bots.bot import Bot

from utils.chess_types import Loyalty, PieceType, TileType
from chess.units.piece import ChessPiece


class RandomBot(Bot):
    """
    A bot that plays random moves.
    """

    def __init__(self, loyalty: Loyalty):
        super().__init__(loyalty)

    def play(self) -> Tuple[Optional[TileType], Optional[ChessPiece]]:
        """
        Play the game automatically by making random moves.
        """
        self.assert_turn() # TODO: Debug? Remove once logic is good.
        
        all_ocs = self.outcomes
        for piece in np.random.permutation(list(all_ocs.keys())):
            p_ocs = all_ocs[piece]
            if not p_ocs: continue
            
            # Choose a random outcome.
            tile = np.random.choice(list(p_ocs.keys()))
            oc = p_ocs[tile]
            
            return tile, oc
            
        print(f'RandomBot {self.loyalty} has no moves.')
        return None, None # No valid moves available, return None or handle stalemate.
