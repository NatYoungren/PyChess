import numpy as np
from enum import Enum


class Piece(Enum):
    NONE = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class TileState(Enum):
    EMPTY = 0
    BLOCKED = 1


class Board:
    def __init__(self, shape=(8, 8)):
        self.shape = shape
        self.board = np.zeros(shape, dtype=int)
        # self.pieces = np.zeros(shape, dtype=int)
        self.default_setup()
    
    def default_setup(self):
        self.board[0] = [4, 2, 3, 5, 6, 3, 2, 4]
        self.board[1] = [1] * 8
        self.board[6] = [-1] * 8
        self.board[7] = [-4, -2, -3, -5, -6, -3, -2, -4]
    
    def is_check(self, test_board, side):
        king_pos = np.where(test_board == side*Piece.KING.value)
        x, y = king_pos[0][0], king_pos[1][0]
        print(x, y)
        pass
    
    def at_tile(self, position):
        # TODO: Implement strange shapes
        return self.board[position] if -self.shape[0] <= position[0] < self.shape[0] and -self.shape[1] <= position[1] < self.shape[1] else None
    
    def viable_moves(self, position):
        selected_piece = self.board[position]
        selected_side = np.sign(selected_piece)
        selected_piece = abs(selected_piece)

        targets = np.zeros(self.shape, dtype=int)
        
        match selected_piece:
            case Piece.PAWN.value:
                # TODO: Account for en passant
                if 0 <= position[0] + selected_side < self.board.shape[0]:
                    targets[position[0] + selected_side, position[1]] = int(self.board[position[0] + selected_side, position[1]] == 0)
                    if position[1] > 0:
                        targets[position[0] + selected_side, position[1]-1] = int(np.sign(self.board[position[0] + selected_side, position[1]-1]) == -selected_side)
                    if position[1] < self.board.shape[1]-1:
                        targets[position[0] + selected_side, position[1]+1] = int(np.sign(self.board[position[0] + selected_side, position[1]+1]) == -selected_side)
                        
            case Piece.KNIGHT.value:
                for m in [-2, 2]:
                    for n in [-1, 1]:
                        if 0 <= position[0] + m < self.board.shape[0] and 0 <= position[1] + n < self.board.shape[1]:
                            targets[position[0] + m, position[1] + n] = int(np.sign(self.board[position[0] + m, position[1] + n]) != selected_side)
                        if 0 <= position[0] + n < self.board.shape[0] and 0 <= position[1] + m < self.board.shape[1]:
                            targets[position[0] + n, position[1] + m] = int(np.sign(self.board[position[0] + n, position[1] + m]) != selected_side)
                            
            case Piece.BISHOP.value:
                for m in [-1, 1]:
                    for n in [-1, 1]:
                        for i in range(1, 8):
                            if 0 <= position[0] + m*i < self.board.shape[0] and 0 <= position[1] + n*i < self.board.shape[1]:
                                targets[position[0] + m*i, position[1] + n*i] = int(np.sign(self.board[position[0] + m*i, position[1] + n*i]) != selected_side)
                                if self.board[position[0] + m*i, position[1] + n*i] != 0:
                                    break
            
            case Piece.ROOK.value:
                for xy in [0, 1]:
                    for n in [-1, 1]:
                        for i in range(1, 8):
                            if 0 <= position[xy] + n*i < self.board.shape[xy]:
                                targets[position[0] + n*i*int(xy==0), position[1] + n*i*int(xy==1)] = int(np.sign(self.board[position[0] + n*i*int(xy==0), position[1] + n*i*int(xy==1)]) != selected_side)
                                if self.board[position[0] + n*i*int(xy==0), position[1] + n*i*int(xy==1)] != 0:
                                    break
                
                
            case Piece.QUEEN.value:
                for m in [-1, 1]:
                    for n in [-1, 1]:
                        for i in range(1, 8):
                            if 0 <= position[0] + m*i < self.board.shape[0] and 0 <= position[1] + n*i < self.board.shape[1]:
                                targets[position[0] + m*i, position[1] + n*i] = int(np.sign(self.board[position[0] + m*i, position[1] + n*i]) != selected_side)
                                if self.board[position[0] + m*i, position[1] + n*i] != 0:
                                    break
                for xy in [0, 1]:
                    for n in [-1, 1]:
                        for i in range(1, 8):
                            if 0 <= position[xy] + n*i < self.board.shape[xy]:
                                targets[position[0] + n*i*int(xy==0), position[1] + n*int(xy==1)] = int(np.sign(self.board[position[0] + n*i*int(xy==0), position[1] + n*i*int(xy==1)]) != selected_side)
                                if self.board[position[0] + n*i*int(xy==0), position[1] + n*i*int(xy==1)] != 0:
                                    break
                
            case Piece.KING.value:
                for m in [-1, 0, 1]:
                    for n in [-1, 0, 1]:
                        if 0 <= position[0] + m < self.board.shape[0] and 0 <= position[1] + n < self.board.shape[1]:
                            targets[position[0] + m, position[1] + n] = int(np.sign(self.board[position[0] + m, position[1] + n]) != selected_side)
                            # TODO: Account for check + castling
                            
            case Piece.NONE.value:
                pass
            
        return targets
    
        
        
if __name__ == "__main__":
    board = Board()
    
    print(board.board)
    print(board.board[0, 0])
    print(board.board[0, 0] == Piece.ROOK.value)
    print(board.viable_moves((0, 1)))
