__author__ = 'alex.krasnyansky'

import math

class ChessBoard:
    vert = 0
    horz = 0
    size = 0
    bit_size = 0

    def __init__(self, vert, horz):
        if vert < 1 or vert > 10 or horz < 1 or horz > 10:
            raise ValueError("Board dimensions must be between 1 and 10, inclusive")
        self.vert = int(vert)
        self.horz = int(horz)
        self.size = vert * horz
        self.bit_size = int(math.ceil(math.log2(self.size)))

    def from_position(self, position):
        i = int(position / self.horz)
        j = position - self.horz * i
        return i, j

    def to_position(self, i, j):
        return i * self.horz + j

    def mirror_1(self, position):
        (i, j) = self.from_position(position)
        return self.to_position(i, self.horz - 1 - j)

    def mirror_2(self, position):
        (i, j) = self.from_position(position)
        return self.to_position(self.vert - 1 - i, j)

    def mirror_3(self, position):
        (i, j) = self.from_position(position)
        return self.to_position(self.vert - 1 - i, self.horz - 1 - j)

    def crop_quarter(self):
        return [pos for pos in range(0, int(math.ceil(self.size / 2))) if pos - self.horz * int(pos / self.horz) < math.ceil(self.horz / 2)]

# Unit Tests

if __name__ == "__main__":
    tp = ChessBoard(2,3).from_position(5)
    assert (1,2) == tp, "Coordinates from pos 5 should be (1,2), and was " + str(tp)
    pos = ChessBoard(2,5).to_position(1,3)
    assert 8 == pos, "Position from (1,3) should be 8, and was " + str(pos)
    bs = ChessBoard(10,10).bit_size
    assert 7 == bs, "Bit size should be 7, and was " + str(bs)
    # Flips odd-sided board
    board = ChessBoard(5,5)
    assert 9 == board.mirror_1(5), "h-flip should be 9, and was " + str(board.mirror_1(5))
    assert 15 == board.mirror_2(5), "v-flip should be 15, and was " + str(board.mirror_2(5))
    assert 19 == board.mirror_3(5), "hv-flip should be 19, and was " + str(board.mirror_3(5))
    assert 16 == board.mirror_1(18), "h-flip should be 16, and was " + str(board.mirror_1(18))
    assert 8 == board.mirror_2(18), "v-flip should be 8, and was " + str(board.mirror_2(18))
    assert 6 == board.mirror_3(18), "hv-flip should be 6, and was " + str(board.mirror_3(18))
    # Flips even-sided board
    board = ChessBoard(2,4)
    assert 0 == board.mirror_1(3), "h-flip should be 0, and was " + str(board.mirror_1(3))
    assert 7 == board.mirror_2(3), "v-flip should be 7, and was " + str(board.mirror_2(3))
    assert 4 == board.mirror_3(3), "hv-flip should be 4, and was " + str(board.mirror_3(3))
    # Cropped quarters
    board = ChessBoard(2,1)
    assert [0] == board.crop_quarter(), "cropped was " + str(board.crop_quarter())
    board = ChessBoard(2,2)
    assert [0] == board.crop_quarter(), "cropped was " + str(board.crop_quarter())
    board = ChessBoard(3,3)
    assert [0, 1, 3, 4] == board.crop_quarter(), "cropped was " + str(board.crop_quarter())
    board = ChessBoard(5,4)
    assert [0, 1, 4, 5, 8, 9] == board.crop_quarter(), "cropped was " + str(board.crop_quarter())


