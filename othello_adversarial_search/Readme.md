# Othello Adversarial Search
Adversarial Search algorithms to play a simple game of Othello.

This program logs the progression of 3 algorithms as they play Othello:
* Greedy
* Min-Max
* Min-Max with Alpha-Beta pruning.

Input format:
An input test cases contains 3 lines followed by the 8x8 board.

The lines:
1. the algorithm to run 1: Greedy, 2: Min-Max, 3: Min-Max with Alpha-Beta pruning.
2. the player you are supposed to represent: either "X" or "O"
3. the cut-off depth of search.

Board: 
An 8x8 matrix of either "*", "X" or "O"; which represent empty-square, player-X & player-O respectively.
