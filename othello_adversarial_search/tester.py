from hw2_veeresh_beeram import *
board = [0] * 64
board[27:29] = [1,-1]
board[35:39] = [-1,1,1,1]
board[20] = -1
board[12] = -1
results = asta_dikpala(35, board, [0,4, 4])
actions_x = action_results_generator((board, 0, [0, 4, 4]), 1)
print ''
