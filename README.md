# chess-placer
A console program in python which finds all possible independent placements of chess pieces on an arbitrary board M*N (9*9 max)

Chess Problem

The problem is to find all distinct layouts of a set of normal chess pieces on a chess board with
dimensions M×N where none of the pieces is in a position to take any of the others. Assume the 
colour of the piece does not matter, and that there are no pawns among the pieces.

Write a program which takes as input:
 The dimensions of the board: M, N.
 The number of pieces of each type (King, Queen, Bishop, Rook and Knight) to try and place 
on the board.

As output, the program should yield the number of distinct layouts for which all of the pieces can be 
placed on the board without threatening each other. 

When returning your solution, please provide with your answer the total number of unique 
configurations for a 6x9 board with 2 Kings, 1 Queen, 1 Bishop, 1 Rook and 1 Knight.
Your solution will need to be able to run on a notebook having 4G RAM.
