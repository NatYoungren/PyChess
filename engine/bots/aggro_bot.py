import numpy as np
from typing import Optional, Tuple, List, Dict

from engine.bots.bot import Bot

from utils.chess_types import Loyalty, PieceType, TileType
from chess.units.piece import ChessPiece

from chess.actions.outcome import Move, Capture
from chess.actions.action import Action

class AggroBot(Bot):
    
    def __init__(self, loyalty: Loyalty):
        super().__init__(loyalty)

    def play(self) -> Tuple[Optional[TileType], Optional[ChessPiece]]:
        """
        Play the game automatically by making random moves.
        """
        self.assert_turn() # TODO: Debug? Remove once logic is good.
        
        all_ocs = self.outcomes
        rand_p_order = np.random.permutation([p for p, k in all_ocs.items() if k])
        
        # TODO: Look for checks!
        
        # Capture selection.
        for piece in rand_p_order:
            # Filter to only Capture outcomes, select randomly.

            p_ocs = all_ocs[piece]
            caps = [t for t, _oc in p_ocs.items() if isinstance(_oc, Capture)]
            if not caps: continue
            
            tile = np.random.choice(caps)
            # TODO: Select the most valuable capture?
            oc = p_ocs[tile]
            
            return tile, oc
        
        # print(f'Aggrobot {self.loyalty} has no captures.')
        
        # If no captures, look for moves.
        for piece in rand_p_order:
            p_ocs = all_ocs[piece]
            # if not p_ocs: continue
            
            # Choose a random outcome.
            tile = np.random.choice(list(p_ocs.keys()))
            oc = p_ocs[tile]
            
            return tile, oc
        
        print(f'Aggrobot {self.loyalty} has no moves.')
        
        return None, None # No valid moves available, return None or handle stalemate.