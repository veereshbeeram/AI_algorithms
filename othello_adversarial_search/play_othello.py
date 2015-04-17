#!/usr/bin/python

import sys
node_names = (
	"a1","b1","c1","d1","e1","f1","g1","h1",
	"a2","b2","c2","d2","e2","f2","g2","h2",
	"a3","b3","c3","d3","e3","f3","g3","h3",
	"a4","b4","c4","d4","e4","f4","g4","h4",
	"a5","b5","c5","d5","e5","f5","g5","h5",
	"a6","b6","c6","d6","e6","f6","g6","h6",
	"a7","b7","c7","d7","e7","f7","g7","h7",
	"a8","b8","c8","d8","e8","f8","g8","h8")

eval_vals = (
	99, -8, 8, 6, 6, 8, -8,99,
	-8,-24,-4,-3,-3,-4,-24,-8,
	 8, -4, 7, 4, 4, 7, -4, 8,
	 6, -3, 4, 0, 0, 4, -3, 6,
	 6, -3, 4, 0, 0, 4, -3, 6,
	 8, -4, 7, 4, 4, 7, -4, 8,
	-8,-24,-4,-3,-3,-4,-24,-8,
	99, -8, 8, 6, 6, 8, -8,99)

inf = 99 * 64
ninf = -1 * inf

def asta_up(position):
	position = position - 8
	if( position >= 0):
		return position
	else:
		return -1

def asta_down(position):
	position = position + 8
	if(position < 64):
		return position
	return -1

def asta_left(position):
	if((position % 8) == 0):
		return -1
	return (position - 1)

def asta_right(position):
	if((position % 8) == 7):
		return -1
	return (position + 1)

def asta_upleft(position):
	if((position % 8) != 0 and (position - 9) >= 0):
		return (position - 9)
	return -1

def asta_downleft(position):
	if((position % 8) != 0 and (position + 7) < 64):
		return (position + 7)
	return -1

def asta_upright(position):
	if((position % 8) != 7 and (position - 7) >= 0):
		return (position - 7)
	return -1


def asta_downright(position):
	if((position % 8) != 7 and (position + 9) < 64):
		return (position + 9)
	return -1

def track(track_player, position, cur_board, direction):
	rl = []
	p = direction(position)
	if(p >=0 and cur_board[p] == track_player):
		rl.append(p)
		rl.extend(track(track_player, p, cur_board, direction))
	return rl

def win_play(player, old_board, oppo_list):
	if(len(oppo_list) <=0):
		return old_board
	blank_pos = oppo_list[-1]
	all_directions = [ asta_up, asta_down,
                           asta_left, asta_right,
                           asta_upleft, asta_upright,
                           asta_downleft, asta_downright ]
	for index in oppo_list:
		old_board[index] = player
	for dir_fun in all_directions:
		ol = track(player * -1, blank_pos, old_board, dir_fun)
		if(len(ol) > 0):
			next_pos = dir_fun(ol[-1])
			if(next_pos >= 0 and old_board[next_pos] == player):
				for index in ol:
					old_board[index] = player 
	return old_board

def asta_dikpala(position,cur_board,counts_xo):
	''' Search all 8 directions for a potential action '''
	results = []
	all_directions = [ asta_up, asta_down, 
			   asta_left, asta_right, 
			   asta_upleft, asta_upright,
			   asta_downleft, asta_downright ]
	cur_player = cur_board[position]
	for dir_fun in all_directions:
		oppo_list = track(cur_player * -1, position, cur_board, dir_fun)
		if(len(oppo_list) > 0):
			blank_pos = dir_fun(oppo_list[-1])
			if(blank_pos >=0 and cur_board[blank_pos] == 0):
				oppo_list.append(blank_pos)
				new_board = win_play(cur_player, cur_board[:], oppo_list) 
				l_counts = counts_xo[:]
				l_counts[cur_player] += len(oppo_list) 
				l_counts[cur_player * -1] -= (len(oppo_list) - 1)
				results.append((new_board, blank_pos,l_counts))
	return results

def action_results_generator(l_state, player_int):
	''' takes a game state & returns list of sorted next actions to examine,
		together with the results of such actions.
		returns tuple of new-board, name and new_counts '''
	cur_board = l_state[0]
	cur_depth = l_state[1]
	counts_xo = l_state[2]
	cur_player = player_int
	if(1 == (cur_depth %2)):
		cur_player = player_int * -1 
	results = []
	for position,player in enumerate(cur_board):
		if(player == cur_player):
			results.extend(asta_dikpala(position,cur_board,counts_xo))
	if(len(results) == 0):
		results.append((cur_board, "pass",counts_xo))
		return results
	else:
		results.sort(key=lambda x: x[1])
		dedup_r = []
		cur_key = 100
		for x in results:
			if(x[1] != cur_key):
				dedup_r.append(x)
				cur_key = x[1]
		return dedup_r
def visualize_board(l_state, p_type):
	''' this needs a list/tuple/array of 64x1 size. prints 8x8 board 
	    There are 2 types: 
			type1: for printing Game represented by *,X,O & block_names
			type2: for printing eval_vals
	'''
	l_board = l_state[0]
	for row in range(0,8):
		this_row = l_board[row*8:row*8+8]
		if(p_type == 1):
			print_row = map(lambda x: "%3s" %x, this_row)
		else:
			print_row = map(lambda x: "%3d" % x,this_row)
		print "-" * 33;
		print "|" +  "|".join(print_row) + "|"
	print "-" * 33

def eval_board(cur_state, player_int):
	''' evaluates the heuristic function for the current board and player turn '''
	cur_board = cur_state[0]
	cur_depth = cur_state[1]
	cur_player = player_int 
	if(1 == (cur_depth % 2)):
		cur_player = -1 * player_int
	return_sum = 0
	#avoiding list comprehensions to keep it compatible with 2.4.2 on aludra
	for state,eval_val in zip(cur_board, eval_vals):
		return_sum = return_sum + (state * eval_val)
	#TODO: Which of these is the correct implementation?
	#return return_sum
	#return cur_player * return_sum
	return player_int * return_sum

def char_recognizer(c):
	if(c == '*'):
		return 0
	else:
		if(c == 'X'):
			return 1
		else:
			return -1
def read_input_txt_file(input_file):
	''' Read the input data from specified file '''
	file_handle = open(input_file,'r') #TODO catch file open errors
	task = int(file_handle.readline().rstrip())
	player_string = file_handle.readline().rstrip()
	cutoff_depth = int(file_handle.readline().rstrip())
	if(task == 1):
		cutoff_depth = 1
	player_int = 1
	if(player_string == "O"):
		player_int = -1
	board = []
	for x in range(0,8):
		internal_board_line = map(lambda y: char_recognizer(y),list(file_handle.readline().rstrip()))
		board.extend(internal_board_line)
	num_x = len(filter(lambda x: x==1, board))
	num_o = len(filter(lambda x: x==-1, board))
	return task, player_int, cutoff_depth, (board,0,[64-(num_x+num_o),num_x,num_o])


# THE alpha beta pruning FUNCTIONS.
def terminal_cutoff_test(state, player_int, cutoff_depth, log_data):
	''' using examplesv2 from TA, the terminal states are:
		* all squares are filled up
		* Only one player has the squares
		* depth == max_depth
	'''
	if(state[1] >= cutoff_depth):
		return True
	counts = state[2]
	if(counts[1] == 0 or counts[-1] == 0 or (counts[1] + counts[-1]) == 64):
		return True
	#check for 2 passes in a row
	if(len(log_data) > 0 and log_data[-1][0] == "pass"):
		actions = action_results_generator(state, player_int)
		if(actions[0][1] == "pass"):
			return True
	return False

def max_value(state, alpha, beta, task, player_int, cutoff_depth, log_data):
	''' state contains:
			0: board
			1: depth
			2: counts
			3: name
	'''
	if(terminal_cutoff_test(state, player_int, cutoff_depth, log_data)):
		# tuple_t = (name, depth, min/max val, alpha, beta)
		ev = eval_board(state, player_int)
		t = (state[3], state[1], ev, alpha, beta)
		log_data.append(t)
		return (state, ev)
	lv = (state,ninf)
	log_data.append((state[3], state[1], lv[1], alpha, beta))
	actions = action_results_generator(state, player_int) 
	for action in actions:
		# each action has (board, name, counts)
		minval = min_value((action[0],state[1]+1,action[2],action[1]), alpha, beta, task, player_int, cutoff_depth, log_data)
		if(minval[1] > lv[1]):
			lv = ((action[0],state[1]+1,action[2],action[1]),minval[1])
			#lv = minval
		if(task == 3 and lv[1] >= beta):
			log_data.append((state[3], state[1], lv[1], alpha, beta))
			return lv
		if(lv[1] > alpha):
			alpha = lv[1]
		log_data.append((state[3], state[1], lv[1], alpha, beta))
	return lv

def min_value(state, alpha , beta, task, player_int, cutoff_depth, log_data):
        if(terminal_cutoff_test(state, player_int, cutoff_depth, log_data)):
                # tuple_t = (name, depth, min/max val, alpha, beta)
                ev = eval_board(state, player_int)
                t = (state[3], state[1], ev, alpha, beta)
                log_data.append(t)
                return (state, ev)
        lv = (state,inf)
        log_data.append((state[3], state[1], lv[1], alpha, beta))
        actions = action_results_generator(state, player_int)
        for action in actions:
		minval = max_value((action[0],state[1]+1,action[2],action[1]), alpha, beta, task, player_int, cutoff_depth, log_data)
		if(minval[1] < lv[1]):
			lv = ((action[0],state[1]+1,action[2],action[1]),minval[1])
			#lv = minval
		if(task == 3 and lv[1] <= alpha):
			log_data.append((state[3], state[1], lv[1], alpha, beta))
			return  lv
		if(lv[1] < beta):
			beta = lv[1]
		log_data.append((state[3], state[1], lv[1], alpha, beta))
	return lv

# THe MAIN Functions
def board_print_string(l_board):
	''' the assignment output spec printer
		pass only game boards of 64x1 '''
	result = []
	for row in range(0,8):
		ps = []
		for col in range(0,8):
			pos = row*8 + col
			if(l_board[pos] == 0):
				ps.append('*')
			else:
				if(l_board[pos] == 1):
					ps.append('X')
				else:
					ps.append('O')
		result.append( "".join(ps))
	return result

def resolve_nodename(node):
	if(node == "root" or node == "pass"):
		return node
	else:
		return node_names[node] 

def print_inf(value):
	if(value == inf):
		return "Infinity"
	else:
		if(value == ninf):
			return "-Infinity"
		else:
			return str(value)

def assignment_mode(task, player_int, cutoff_depth, init_state):
	log_data = []
	choice = max_value((init_state[0],init_state[1],init_state[2],"root") , ninf, inf, task, player_int, cutoff_depth, log_data)
	output_lines = board_print_string(choice[0][0])
	if(task == 2):
		output_lines.append("Node,Depth,Value")
		for log in log_data:
			output_lines.append(",".join([ resolve_nodename(log[0]), str(log[1]), print_inf(log[2]) ]))
	if(task == 3):
		output_lines.append("Node,Depth,Value,Alpha,Beta")
		for log in log_data:
			output_lines.append(",".join(
				[ resolve_nodename(log[0]), str(log[1]), print_inf(log[2]),
					print_inf(log[3]), print_inf(log[4]) ]))
	file_handle = open("output.txt","w") #TODO error checking for file
	file_handle.write("\n".join(output_lines))
	file_handle.close()

def competition_mode():
	return


if __name__ == "__main__":
	task, player_int, cutoff_depth, init_state = read_input_txt_file("input.txt")
	if(task != 4):
		assignment_mode(task, player_int, cutoff_depth, init_state)
	else:
		competition_mode()
