__author__ = 'alex.krasnyansky'

from PlacementCypher import *
import time
import argparse


def print_position(code):
    if not is_quiet:
        print("Position", code)
    if not is_no_file:
        text_out.write("Position %d\n" % code)
    for line in to_lines(board, code):
        if not is_quiet:
            print(line)
        if not is_no_file:
            text_out.write(line+'\n')
    if not is_quiet:
        print()
    if not is_no_file:
        text_out.write('\n')


def put_piece(pieces, p, free_cells, start_cell):
    global iterations
    is_ok = False
    for free_pos in free_cells:
        if free_pos < start_cell:  # To move on to the next solution, skip as many free cells as have been tried before
            continue
        #  Put the current piece in the current available free cell
        pieces[p].put(free_pos)
        iterations += 1
        #  Check that the just put piece does not hit anything placed before
        is_ok = not any(pieces[prev_piece].is_hit_by(pieces[p]) for prev_piece in range(0, p))
        if is_ok:
            break
    if not is_ok:  # In case the putting was wrong, unset the piece
        pieces[p].put(-1)
    return is_ok


def find_placements(p, p_free_cells):
    cnt = 0
    fives = 0
    # Optimization: move the 1st piece only inside top-left quarter of the board, mirror solution to 3 possible flips
    if p == 0:
        free_cells = pieces[p].crop_quarter()
    else:
        free_cells = p_free_cells
    for start_cell in free_cells:
        # Progress is tracked by movement of the 1st piece
        if p == 0:
            cnt += 1
            progress = 100.0 * cnt / len(free_cells)
            if int(progress / 5) > fives:
                fives = int(progress / 5)
                print("Search is about %d%% done - %d iterations done, %d placements found" % (fives * 5, iterations, len(found_placements)))
        if put_piece(pieces, p, free_cells, start_cell):
            # Is a full placement found?
            if p == len(pieces) - 1:
                (cypher_0, cypher_1, cypher_2, cypher_3) = cyphers(board, pieces)
                # Register one straight solution and 3 symmetric
                found_placements.add(cypher_0)
                found_placements.add(cypher_1)
                found_placements.add(cypher_2)
                found_placements.add(cypher_3)
            if p < len(pieces) - 1:
                find_placements(p + 1, pieces[p].free_cells(p_free_cells))

# board = ChessBoard(2,2)
# pieces = [Bishop(board), Bishop(board)]

# board = ChessBoard(3,3)
# pieces = [King(board), Rook(board), King(board)]

# board = ChessBoard(4,5)
# pieces = [Queen(board), Rook(board), Bishop(board), King(board)]

# board = ChessBoard(7,6)
# pieces = [Queen(board), Queen(board), Queen(board), Bishop(board), Bishop(board)]

# board = ChessBoard(6,9)
# pieces = [Queen(board), Rook(board), Bishop(board), King(board), King(board), Knight(board)]

# Take command-line arguments
parser = argparse.ArgumentParser(description="Finds unique independent placements of chess pieces on a "\
    "rectangular chess board. Independent placements are such in which no chess pieces can take each other.")
parser.add_argument("ht", type=int, help="the chess board height (1..10)")
parser.add_argument("wt", type=int, help="the chess board width (1..10)")
parser.add_argument("-nc", "--no_console", help="suppress console output for placements (false by default)", action="store_true")
parser.add_argument("-o", "--out_file", help="file name to send output to", type=str, default=None)
parser.add_argument("-k", "--kings", type=int, default=0, help="how many Kings to put")
parser.add_argument("-q", "--queens", type=int, default=0, help="how many Queens to put")
parser.add_argument("-r", "--rooks", type=int, default=0, help="how many Rooks to put")
parser.add_argument("-b", "--bishops", type=int, default=0, help="how many Bishops to put")
parser.add_argument("-s", "--knights", type=int, default=0, help="how many Knights to put")
args = parser.parse_args()

# Validate inputs
if args.ht < 1:
    print("Error: board height can't be less than 1")
    exit(1)
if args.ht > 10:
    print("Error: board height more than 10 not allowed")
    exit(1)
if args.wt < 1:
    print("Error: board width can't be less than 1")
    exit(1)
if args.wt > 10:
    print("Error: board width more than 10 not allowed")
    exit(1)

# Make the board
board = ChessBoard(args.ht, args.wt)

# How to output
is_quiet = args.no_console
is_no_file = args.out_file is None
is_print_placements = not is_quiet or not is_no_file
filename = args.out_file

# Creating pieces in the heuristic order (taking most space come first)
pieces = []
for _ in range(args.queens):
    pieces.append(Queen(board))
for _ in range(args.rooks):
    pieces.append(Rook(board))
for _ in range(args.bishops):
    pieces.append(Bishop(board))
for _ in range(args.kings):
    pieces.append(King(board))
for _ in range(args.knights):
    pieces.append(Knight(board))

# Validate pieces
if len(pieces) == 0:
    print("Error: there should be at least one chess piece to put, you specified none")
    exit(1)
if len(pieces) > math.ceil(board.size / 2):
    print("Error: you specified total %d pieces, which is more than half of the board cells, %d."\
          " Try lesser number." % (len(pieces), math.ceil(board.size / 2)))
    exit(1)

# Do the work
found_placements = set()
start = time.time()
iterations = 0
find_placements(0, list(range(0, board.size)))  # Start with piece 0 and completely free board
duration = time.time() - start
result = ["-" * 30 + '\n', "Total Placements Found: %d\n" % len(found_placements),
          "Iterations Spent: %d\n" % iterations,
          "Calculation Duration was %d seconds\n\n" % duration]

# Optional output
if is_print_placements:
    if not is_no_file:
        with open(filename, "w") as text_out:
            for line in result:
                text_out.write(line)
                if not is_quiet:
                    print(line)
            for code in found_placements:
                print_position(code)
    else:
        for line in result:
            print(line)
        for code in found_placements:
            print_position(code)
