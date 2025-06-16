import numpy as np
from typing import Optional, Tuple, List, Dict

from utils.chess_types import Loyalty, PieceType, TileType
from chess.units.piece import ChessPiece
from chess.tiles.tile import Tile
from chess.actions.outcome import Outcome, Move, Capture

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
    
    piece_values: Dict[PieceType, float] = {
        PieceType.PAWN: 1.0,
        PieceType.KNIGHT: 3.0,
        PieceType.BISHOP: 3.0,
        PieceType.ROOK: 5.0,
        PieceType.QUEEN: 9.0,
        PieceType.KING: 100.0,  # King is invaluable.
        PieceType.SUMMONER: 4.0,  # Example value for a Summoner piece.
        PieceType.ZOMBIE: 2.0,  # Example value for a Zombie piece.
        PieceType.JESTER: 4.0,  # Example value for a Jester piece.
        PieceType.SENTRY: 4.0,  # Example value for a Sentry piece.
    }
    
    
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
    def disloyal_pieces(self) -> List[ChessPiece]:
        return self.board.disloyal_pieces(self.loyalty)
    
    @property
    def outcomes(self) -> Dict[ChessPiece, Dict[Tile, List[ChessPiece]]]:
        return {p: p.outcomes for p in self.pieces}
        
    def assert_turn(self):
        if self.board.current_turn != self.loyalty:
            raise ValueError(f"Bot {self.loyalty} cannot play on {self.board.current_turn} turn.")

    def play(self) -> Tuple[Optional[Tile], Optional[ChessPiece]]:
        raise NotImplementedError("This method should be implemented by subclasses.")


    # TODO: More thinking on player turn leads to more depth during bot eval?
    #       Use some threading to allow bot to think constantly?
    #       Imagine a slowed down version of the 'chess-engine' eval where it shows the best move.
    #       You see the bots current choice (of move, or of piece-to-move) and it updates that preview as you take more time.
    #       This would need to be dramatized to make it more engaging.
    #       Caching the decision tree may be a bit excessive, but could be useful?
    
    #       TUTORIAL:
    #           Quickly quickly, push the advantage my lord! Combat can be messy.
    #           HALT, look carefully! We've broken their formation.
    #           Victory in this battle is certain with the right tactics, but we must be careful.
    
    # Have bots consider moves of certain pieces?
    #   Overlook other pieces?
    #   How much value should be placed on 'morale'?
    def eval_outcome(self, outcome: Outcome, depth: int = 0) -> float:
        """
        Evaluate the outcome of a move.
        This is a placeholder for actual evaluation logic.
        """
        return np.random.uniform() # Placeholder evaluation logic
        
    # TODO: Is depth worth considering here?
    #       Or focus on 'immediate' check avoidance.
    def safe_outcomes(self, depth: int = 0) -> Dict[ChessPiece, Dict[Tile, Outcome]]:
        pass
    
    def count_material(self, l: Optional[Loyalty]=None) -> float:
        """
        Count the material value of the bot's pieces.
        """
        if l is None: l = self.loyalty
        material_count = 0.0
        for faction in self.board.turn_order:
            scalar = 1.0 if faction == l else -1.0
            for piece in self.board.loyal_pieces(faction):
                material_count += self.piece_values.get(piece.piece_type, 0) * scalar

        return material_count
    
    # attack_counts : Must consider 'x-ray' and turn order?
    # defend_counts : Must consider 'x-ray' and turn order?
    