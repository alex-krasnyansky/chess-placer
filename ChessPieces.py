__author__ = 'alex.krasnyansky'

from ChessBoard import *

codes = {1:'Q', 2:'R', 3:'B', 4:'K', 5:'S'}


class ChessPiece:
    position = -1
    board = None
    reached_cells = None

    def __init__(self, board):
        self.board = board

    def put(self, position):
        self.position = position
        self.spread_cells()

    def spread_cells(self):
        pass

    def num_code(self):
        pass

    def free_cells(self, pre_free_cells):
        new_free_cells = list(set(pre_free_cells).difference(self.reached_cells))
        new_free_cells.sort()
        return new_free_cells

    def crop_quarter(self):
        return self.board.crop_quarter()

    def is_hit_by(self, another):
        return self.position in another.reached_cells


class Queen(ChessPiece):

    def spread_cells(self):
        self.reached_cells = set()
        if self.position < 0:
            return
        (i0, j0) = self.board.from_position(self.position)
        for i in range(0, self.board.vert):
            self.reached_cells.add(self.board.to_position(i, j0))
            left = j0 - abs(i - i0)
            right = j0 + abs(i - i0)
            if left >= 0:
                self.reached_cells.add(self.board.to_position(i, left))
            if right < self.board.horz:
                self.reached_cells.add(self.board.to_position(i, right))
        for j in range(0, self.board.horz):
            self.reached_cells.add(self.board.to_position(i0, j))

    def num_code(self):
        return 1  # 001


class Rook(ChessPiece):

    def spread_cells(self):
        self.reached_cells = set()
        if self.position < 0:
            return
        (i0, j0) = self.board.from_position(self.position)
        for i in range(0, self.board.vert):
            self.reached_cells.add(self.board.to_position(i, j0))
        for j in range(0, self.board.horz):
            self.reached_cells.add(self.board.to_position(i0, j))

    def num_code(self):
        return 2  # 010


class Bishop(ChessPiece):

    def spread_cells(self):
        self.reached_cells = set()
        if self.position < 0:
            return
        (i0, j0) = self.board.from_position(self.position)
        for i in range(0, self.board.vert):
            left = j0 - abs(i - i0)
            right = j0 + abs(i - i0)
            if left >= 0:
                self.reached_cells.add(self.board.to_position(i, left))
            if right < self.board.horz:
                self.reached_cells.add(self.board.to_position(i, right))

    def num_code(self):
        return 3  # 011


class King(ChessPiece):

    def spread_cells(self):
        self.reached_cells = set()
        if self.position < 0:
            return
        (i0, j0) = self.board.from_position(self.position)
        min_i = max(0, i0 - 1)
        max_i = min(self.board.vert-1, i0 + 1)
        min_j = max(0, j0 - 1)
        max_j = min(self.board.horz-1, j0 + 1)
        for i in range(min_i, max_i + 1):
            for j in range(min_j, max_j + 1):
                self.reached_cells.add(self.board.to_position(i, j))

    def num_code(self):
        return 4  # 100


class Knight(ChessPiece):

    def spread_cells(self):
        self.reached_cells = set()
        if self.position < 0:
            return
        (i0, j0) = self.board.from_position(self.position)
        self.reached_cells.add(self.board.to_position(i0, j0))
        if i0 - 2 >= 0:
            if j0 - 1 >= 0:
                self.reached_cells.add(self.board.to_position(i0 - 2, j0 - 1))
            if j0 + 1 < self.board.horz:
                self.reached_cells.add(self.board.to_position(i0 - 2, j0 + 1))
        if i0 - 1 >= 0:
            if j0 - 2 >= 0:
                self.reached_cells.add(self.board.to_position(i0 - 1, j0 - 2))
            if j0 + 2 < self.board.horz:
                self.reached_cells.add(self.board.to_position(i0 - 1, j0 + 2))
        if i0 + 1 < self.board.vert:
            if j0 - 2 >= 0:
                self.reached_cells.add(self.board.to_position(i0 + 1, j0 - 2))
            if j0 + 2 < self.board.horz:
                self.reached_cells.add(self.board.to_position(i0 + 1, j0 + 2))
        if i0 + 2 < self.board.vert:
            if j0 - 1 >= 0:
                self.reached_cells.add(self.board.to_position(i0 + 2, j0 - 1))
            if j0 + 1 < self.board.horz:
                self.reached_cells.add(self.board.to_position(i0 + 2, j0 + 1))

    def num_code(self):
        return 5  # 101


# Unit Tests

# The test board layout is:

#      0  1  2  3  4
#     __ __ __ __ __
# 0 |  0  1  2  3  4
# 1 |  5  6  7  8  9
# 2 | 10 11 12 13 14
# 3 | 15 16 17 18 19
# 4 | 20 21 22 23 24

# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

if __name__ == "__main__":
    board = ChessBoard(5,5)
    all_free_cells = list(range(0, board.size))

    # Knight middle
    knight = Knight(board)
    knight.put(12)
    assert knight.reached_cells == {1, 3, 5, 9, 12, 15, 19, 21, 23}
    assert knight.free_cells(all_free_cells) == [0, 2, 4, 6, 7, 8, 10, 11, 13, 14, 16, 17, 18, 20, 22, 24]

    # Knight corner
    knight.put(1)
    assert knight.reached_cells == {1, 8, 10, 12}
    assert knight.free_cells(all_free_cells) == [0, 2, 3, 4, 5, 6, 7, 9, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    # Queen middle
    queen = Queen(board)
    queen.put(12)
    assert queen.reached_cells == {0, 2, 4, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 20, 22, 24}
    assert queen.free_cells(all_free_cells) == [1, 3, 5, 9, 15, 19, 21, 23]

    # Queen corner
    queen.put(19)
    assert queen.reached_cells == {1, 4, 7, 9, 13, 14, 15, 16, 17, 18, 19, 23, 24}
    assert queen.free_cells(all_free_cells) == [0, 2, 3, 5, 6, 8, 10, 11, 12, 20, 21, 22]

    # Bishop middle
    bishop = Bishop(board)
    bishop.put(16)
    assert bishop.reached_cells == {4, 8, 10, 12, 16, 20, 22}
    assert bishop.free_cells(all_free_cells) == [0, 1, 2, 3, 5, 6, 7, 9, 11, 13, 14, 15, 17, 18, 19, 21, 23, 24]

    # Bishop corner
    bishop.put(0)
    assert bishop.reached_cells == {0, 6, 12, 18, 24}
    assert bishop.free_cells(all_free_cells) == [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23]

    # King middle
    king = King(board)
    king.put(8)
    assert king.reached_cells == {2, 3, 4, 7, 8, 9, 12, 13, 14}
    assert king.free_cells(all_free_cells) == [0, 1, 5, 6, 10, 11, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    # King corner
    king.put(24)
    assert king.reached_cells == {18, 19, 23, 24}
    assert king.free_cells(all_free_cells) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22]

    # Rook middle
    rook = Rook(board)
    rook.put(12)
    assert rook.reached_cells == {2, 7, 10, 11, 12, 13, 14, 17, 22}
    assert rook.free_cells(all_free_cells) == [0, 1, 3, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 23, 24]

    # Rook corner
    rook.put(20)
    assert rook.reached_cells == {0, 5, 10, 15, 20, 21, 22, 23, 24}
    assert rook.free_cells(all_free_cells) == [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19]

    # Clearing case
    queen.put(-1)
    assert queen.reached_cells == set()
    assert queen.free_cells(all_free_cells) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]