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
        evals = []
        # best_oc = None
        for piece in np.random.permutation(list(all_ocs.keys())):
            for tile, oc in all_ocs[piece].items(): # TODO: Store tile in oc?
                evals.append((self.eval_outcome(oc), piece, tile, oc)) # TODO: Less?
            
        if evals:
            evals.sort(key=lambda x: x[0], reverse=True)
            best_eval, piece, tile, oc = evals[0]
            print(f'RandomBot {self.loyalty} playing: {piece.name} -> {tile} with outcome {oc}')
            print(f'Evaluation: {best_eval}\n')
            return tile, oc
        
        print(f'RandomBot {self.loyalty} has no moves.')
        return None, None # No valid moves available, return None or handle stalemate.
