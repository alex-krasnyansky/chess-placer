__author__ = 'alex.krasnyansky'

from ChessPieces import *


def cyphers(board, pieces):
    flip_0 = 0
    flip_1 = 0
    flip_2 = 0
    flip_3 = 0
    full_shift = 3 + board.bit_size
    occupied_0 = [(cp, pieces[cp].position) for cp in range(0, len(pieces))]
    occupied_1 = [(cp, board.mirror_1(pieces[cp].position)) for cp in range(0, len(pieces))]
    occupied_2 = [(cp, board.mirror_2(pieces[cp].position)) for cp in range(0, len(pieces))]
    occupied_3 = [(cp, board.mirror_3(pieces[cp].position)) for cp in range(0, len(pieces))]
    occupied_0.sort(key=lambda tup: tup[1])
    occupied_1.sort(key=lambda tup: tup[1])
    occupied_2.sort(key=lambda tup: tup[1])
    occupied_3.sort(key=lambda tup: tup[1])
    for index in range(0, len(occupied_0)):
        # straight
        (cp, pos) = occupied_0[index]
        code = pieces[cp].num_code() << board.bit_size
        cypher_0 = code | pos
        flip_0 = (flip_0 << full_shift) | cypher_0
        # flip 1
        (cp, pos) = occupied_1[index]
        code = pieces[cp].num_code() << board.bit_size
        cypher_1 = code | pos
        flip_1 = (flip_1 << full_shift) | cypher_1
        # flip 2
        (cp, pos) = occupied_2[index]
        code = pieces[cp].num_code() << board.bit_size
        cypher_2 = code | pos
        flip_2 = (flip_2 << full_shift) | cypher_2
        # flip 3
        (cp, pos) = occupied_3[index]
        code = pieces[cp].num_code() << board.bit_size
        cypher_3 = code | pos
        flip_3 = (flip_3 << full_shift) | cypher_3
    return flip_0, flip_1, flip_2, flip_3


def to_lines(board, cyphered):
    # Init masks
    full_shift = 3 + board.bit_size
    full_mask = 2 ** full_shift - 1
    piece_mask = 7 << (full_shift - 3)
    position_mask = ~piece_mask
    positions = {} # Dictionary of filled in positions, contains piece characters
    # Decyphering
    while cyphered > 0:
        part = cyphered & full_mask
        cyphered = cyphered >> full_shift
        piece_code = (part & piece_mask) >> (full_shift - 3)
        position = part & position_mask
        piece_char = codes.get(piece_code)
        positions[position] = piece_char
    # Making lines
    lines = []
    # We'll be okay with board ascii formats when boards are less than 10 by any side
    lines.append("    " + ' '.join(map(str, (range(0, board.horz)))))
    lines.append("   " + " _" * board.horz)
    for i in range(0, board.vert):
        line = [str(i)," |"]
        for j in range(0, board.horz):
            line.append(' ')
            cur_pos = board.to_position(i,j)
            if cur_pos in positions:
                line.append(positions.get(cur_pos))
            else:
                line.append('.')
        lines.append(''.join(line))
    return lines

# Unit Tests

if __name__ == "__main__":

    # Test 1
    #     0 1       0 1       0 1       0 1
    #     _ _       _ _       _ _       _ _
    # 0 | Q .   0 | . Q   0 | . R   0 | R .
    # 1 | . R   1 | R .   1 | Q .   1 | . Q
    #
    # Q = 001 | 00    001 | 01    001 | 10   001 | 11
    # R = 010 | 11    010 | 10    010 | 01   010 | 00
    #
    # Ordered by increased position number:
    # cypher_0 = 00100 01011 = int('0010001011',2) = 139
    # cypher_1 = 00101 01010 = int('0010101010',2) = 170
    # cypher_2 = 01001 00110 = int('0100100110',2) = 294
    # cypher_3 = 01000 00111 = int('0100000111',2) = 263
    board = ChessBoard(2,2)
    queen = Queen(board)
    queen.put(0)
    rook = Rook(board)
    rook.put(3)
    pieces = [queen, rook]
    assert cyphers(board,pieces) == (139, 170, 294, 263), "Expected values were (139, 170, 294, 263), actually " + str(cyphers(board,pieces))

    # Test 2
    #     0 1       0 1       0 1       0 1
    #     _ _       _ _       _ _       _ _
    # 0 | R .   0 | . R   0 | . R   0 | R .
    # 1 | . R   1 | R .   1 | R .   1 | . R
    #
    # R = 010 | 00    010 | 01    010 | 01    010 | 00
    # R = 010 | 11    010 | 10    010 | 10    010 | 11
    #
    # Ordered by increased position number:
    # cypher_0 = 01000 01011 = int('0100001011',2) = 267
    # cypher_1 = 01001 01010 = int('0100101010',2) = 298
    # cypher_2 = 01001 01010 = int('0100101010',2) = 298
    # cypher_3 = 01000 01011 = int('0100001011',2) = 267
    board = ChessBoard(2,2)
    rook1 = Rook(board)
    rook1.put(0)
    rook2 = Rook(board)
    rook2.put(3)
    pieces = [rook1, rook2]
    assert cyphers(board,pieces) == (267, 298, 298, 267), "Expected values were (267, 298, 298, 267), actually " + str(cyphers(board,pieces))
    # Reversed
    pieces = [rook2, rook1]
    assert cyphers(board,pieces) == (267, 298, 298, 267), "Expected values were (267, 298, 298, 267), actually " + str(cyphers(board,pieces))

    # Test 3
    #     0 1 2 3       0 1 2 3       0 1 2 3       0 1 2 3
    #     _ _ _ _       _ _ _ _       _ _ _ _       _ _ _ _
    # 0 | . . R .   0 | . R . .   0 | . . . K   0 | K . . .
    # 1 | B . . .   1 | . . . B   1 | B . . .   1 | . . . B
    # 2 | . . . K   2 | K . . .   2 | . . R .   2 | . R . .
    #
    # R = 010 | 0010    010 | 0001    010 | 1010    010 | 1001
    # B = 011 | 0100    011 | 0111    011 | 0100    011 | 0111
    # K = 100 | 1011    100 | 1000    100 | 0011    100 | 0000
    #
    # Ordered by increased position number:
    # cypher_0 = 0100010 0110100 1001011 = int('010001001101001001011',2) = 563787
    # cypher_1 = 0100001 0110111 1001000 = int('010000101101111001000',2) = 547784
    # cypher_2 = 1000011 0110100 0101010 = int('100001101101000101010',2) = 1104426
    # cypher_3 = 1000000 0110111 0101001 = int('100000001101110101001',2) = 1055657
    board = ChessBoard(3,4)
    rook = Rook(board)
    rook.put(2)
    bishop = Bishop(board)
    bishop.put(4)
    king = King(board)
    king.put(11)
    pieces = [rook, bishop, king]

    assert cyphers(board,pieces) == (563787, 547784, 1104426, 1055657), "Expected values were (563787, 547784, 1104426, 1055657), actually " + str(cyphers(board,pieces))

    # Test 4
    board = ChessBoard(2,2)
    lines = to_lines(board, 139)
    assert len(lines) == 4
    assert "    0 1" == lines[0]
    assert "    _ _" == lines[1]
    assert "0 | Q ." == lines[2]
    assert "1 | . R" == lines[3]

    # Test 5
    board = ChessBoard(3,4)
    lines = to_lines(board, 563787)
    assert len(lines) == 5
    assert "    0 1 2 3" == lines[0]
    assert "    _ _ _ _" == lines[1]
    assert "0 | . . R ." == lines[2]
    assert "1 | B . . ." == lines[3]
    assert "2 | . . . K" == lines[4]


