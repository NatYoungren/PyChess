import numpy as np
from typing import Tuple

from utils.chess_types import Position, Vector
from utils.chess_types import DirCls as D
from utils.chess_types import Loyalty, PieceType

from chess.units.piece import ChessPiece
from chess.actions.action import Action
from chess.actions.outcome import Move, Capture, MultiMove, MultiCapture

# TODO: Simplify, when moving between 2 pieces all three are destroyed?
class BerserkerMoveOnly(Action):
    """
    Represents a move action for a Berserker.
    """
    
    def flag_enpassant(self):
        self.piece.en_passantable = True
        
    def update(self):
        super().update()
        poss_moves = self.get_line(D.f,
                              length=2,
                              enemy_ok=False)
        for i, (pos, t, p) in enumerate(poss_moves):
            self.add_outcome(t, Move(self.piece, pos, callback = self.flag_enpassant if i==1 else lambda: None))


class BerserkerCaptureOnly(Action):
    """
    Represents a capture action for a Berserker.
    """
    
    def a_warriors_death(self):
        """
        Callback to ensure Berserker's death after a double capture.
        """
        self.board.get_tile(self.piece.position).piece = None
    
    def update(self):
        super().update()
        for v in (D.f_l, D.f_r):
            for pos, t, p in self.get_line(v, length=1, can_move=False):
                self.add_outcome(t, Capture(self.piece, pos, p))
                
                # Berserkers can capture 2 pieces at once diagonally, but die in the process.
                for posD, tD, pD in self.get_line(v, start=pos, length=1, can_move=False):
                    self.add_outcome(tD, Capture(self.piece, posD, (p, pD, self.piece), l_delta=-1, callback=self.a_warriors_death))


# class PawnPassant(Action):
#     """
#     Represents an en passant capture action for a pawn.
#     """
    
#     def update(self):
#         super().update()
#         for hv, dv in ((D.l, D.f_l), (D.r, D.f_r)):
#             for pos, t, p in self.get_line(hv,
#                                            length=1,
#                                            can_move=False):
#                 if isinstance(p, Pawn) and p.loyalty != self.piece.loyalty and p.en_passantable:
#                     for posD, tD, pD in self.get_line(dv, length=1, can_move=True, enemy_ok=False):
#                         self.add_outcome(tD, Capture(self.piece, posD, p, l_delta=2))
#                         # break
                    
# class ShieldWallAdvance(Action):
#     """
#     Represents a special action for pawns to advance in a shield wall formation.
#     This is a custom action that allows pawns to move forward in a coordinated manner.
#     """
    
#     def update(self):
#         super().update()
#         # Implement the logic for shield wall advancement here.
#         # For example, allow pawns to move forward only if they are adjacent to another pawn.
#         advancing_pieces = []
#         piece_targets = []
        
#         pos_t_p = self.get_line(D.f, length=1, can_move=True, enemy_ok=False)  # Get the tile in front of the pawn
#         if len(pos_t_p) == 0: return
#         pos, t, p = pos_t_p[0]
#         if t is None or p is not None: return # If the tile is out of bounds or occupied
#         advancing_pieces.append(self.piece)  # Add the pawn to the advancing pieces
#         piece_targets.append(pos)
        
#         for dx in (D.l, D.r):  # Move pawns up to one square left and right
#             dx = self.orient_vector(dx)
#             dpos = self.piece.position + dx
#             dt, dp = self.board.at_pos(dpos)
#             if dt is None or dp is None:
#                 continue
            
#             is_pawn = isinstance(dp, Pawn) and dp.loyalty == self.piece.loyalty
#             if not is_pawn: continue
                        
#             pos_t_p = dp.get_line(D.f, length=1, can_move=True, enemy_ok=False)  # Get the tile in front of the pawn
#             if len(pos_t_p) == 0: continue
#             pos, t, p = pos_t_p[0]
#             if t is None or p is not None: continue # If the tile is out of bounds or occupied
            
#             advancing_pieces.append(dp)  # Add the pawn to the advancing pieces
#             piece_targets.append(pos)
            
#         if len(advancing_pieces) < 2: return # Only advance when at least one adjacent pawn can come with.
#         self.add_outcome(self.board[self.piece.position], MultiMove(advancing_pieces, piece_targets, callback=lambda: None))  # Execute the advance action

# class ChainCapture(Action):
#     """
#     Represents a chain capture action for pawns.
#     This allows diagonally connected pawns to capture together, staying connected while shifting in the direction of the chain.
#     """
    
#     def update(self):
#         super().update()
        
#         for v in (D.f_l, D.f_r):
#             pawn_chain = [self.piece]
#             target_chain = []
#             target_tile = None
#             for pos, t, p in self.get_line(v,
#                                            length=8,
#                                            can_move=True,
#                                            ally_ok=True,
#                                            jump_ally=True):
#                 if isinstance(p, Pawn) and p.loyalty == self.piece.loyalty:
#                     # Need data of 'start' -> 'end' position for each pawn.
#                     # Or, 'piece' -> 'target' position.
#                     pawn_chain.append(p)
#                     target_chain.append(pos)
#                     continue
#                 elif isinstance(p, ChessPiece) and p.loyalty != self.piece.loyalty:
#                     if target_chain:
#                         target_tile = t
#                         target_chain.append(pos)
#                     break
#                 break
            
#             if target_tile is None: # Cannot act if no target or pawn_chain
#                 continue
            
#             self.add_outcome(target_tile, MultiCapture(pawn_chain, target_chain,
#                                                      captured=[target_tile.piece], callback=lambda: None,
#                                                      l_delta=-(len(pawn_chain) - 1)))
#         # TODO: Shift all pawns in order of furthest to self.piece.
    

# Allow en-passant?
class Berserker(ChessPiece):
    en_passantable: bool
    
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.BERSERKER, position=position)
        self.en_passantable = False
        self.actions.append(BerserkerMoveOnly(self))
        self.actions.append(BerserkerCaptureOnly(self))
        # self.actions.append(PawnPassant(self))
        # self.actions.append(ShieldWallAdvance(self))
        # self.actions.append(ChainCapture(self))

    def turn_changed(self):
        if self.board.current_turn == self.loyalty:
            self.en_passantable = False
        super().turn_changed()