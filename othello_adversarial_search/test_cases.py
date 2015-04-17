#!/usr/bin/python

import unittest
from hw2_veeresh_beeram import *

class HW2Testing(unittest.TestCase):
	def test_directions(self):
		self.assertEqual(asta_up(50), 42)
		self.assertEqual(asta_up(4), -1)

		self.assertEqual(asta_down(34), 42)
		self.assertEqual(asta_down(60), -1)

		self.assertEqual(asta_left(23), 22)
		self.assertEqual(asta_left(24), -1)

		self.assertEqual(asta_right(32), 33)
		self.assertEqual(asta_right(31), -1)

		self.assertEqual(asta_upleft(6), -1)
		self.assertEqual(asta_upleft(0), -1)
		self.assertEqual(asta_upleft(16), -1)
		self.assertEqual(asta_upleft(20), 11)

		self.assertEqual(asta_upright(1), -1)
		self.assertEqual(asta_upright(15), -1)
		self.assertEqual(asta_upright(7), -1)
		self.assertEqual(asta_upright(30), 23)

		self.assertEqual(asta_downleft(56), -1)
		self.assertEqual(asta_downleft(48), -1)
		self.assertEqual(asta_downleft(59), -1)
		self.assertEqual(asta_downleft(26), 33)

		self.assertEqual(asta_downright(63), -1)
		self.assertEqual(asta_downright(61), -1)
		self.assertEqual(asta_downright(47), -1)
		self.assertEqual(asta_downright(19), 28)

	def test_tracking(self):
		board = [0] * 64
		board[27:29] = [1,-1]
		board[35:40] = [-1,1,1,1,1]
		board[20] = -1
		board[12] = -1
		self.assertEqual(track(-1,36,board,asta_up),[28,20,12])
		self.assertEqual(track(-1,36,board,asta_down),[])
		self.assertEqual(track(-1,36,board,asta_left),[35])
		self.assertEqual(track(-1,36,board,asta_right),[])
		self.assertEqual(track(-1,36,board,asta_upleft),[])
		self.assertEqual(track(-1,36,board,asta_downleft),[])
		self.assertEqual(track(-1,36,board,asta_upright),[])
		self.assertEqual(track(-1,36,board,asta_downright),[])
		

		self.assertEqual(track(1,36,board,asta_up),[])
		self.assertEqual(track(1,36,board,asta_down),[])
		self.assertEqual(track(1,36,board,asta_left),[])
		self.assertEqual(track(1,36,board,asta_right),[37,38,39])
		self.assertEqual(track(1,36,board,asta_upleft),[27])
		self.assertEqual(track(1,36,board,asta_downleft),[])
		self.assertEqual(track(1,36,board,asta_upright),[])
		self.assertEqual(track(1,36,board,asta_downright),[])

		self.assertEqual(track(1,33,board,asta_up),[])
		self.assertEqual(track(1,33,board,asta_down),[])
		self.assertEqual(track(1,33,board,asta_left),[])
		self.assertEqual(track(1,33,board,asta_right),[])
		self.assertEqual(track(1,33,board,asta_upleft),[])
		self.assertEqual(track(1,33,board,asta_downleft),[])
		self.assertEqual(track(1,33,board,asta_upright),[])
		self.assertEqual(track(1,33,board,asta_downright),[])

		new_board = win_play(1,board,[])
		self.assertEqual(new_board,board)
		new_board = win_play(1,board,track(1,35,board,asta_right))
		board[35:40] = [-1] * 5
		self.assertEqual(new_board, board)
		
		tb = [0]*64
		tb[56] = -1; tb[49:51] = [1,1]; tb[42:44] = [-1,1]; tb[35:37] = [-1,1]
		tb[28:30] =  [-1,1]; tb[21:23] =  [-1,1]; tb[14:16] =  [-1,1];
		new_board = win_play(1,tb,[14,13])
		tb[13:15] = [1] * 2
		tb[21] = 1
		self.assertEqual(new_board, tb)
		tb = [0] * 64
		tb[1:6] = [1] * 5
		tb[9:14] = [-1] * 5
		tb[25:30] = [-1] * 5
		tb[33:38] = [1] * 5
		new_board = win_play(1,tb,[11,19])
		tb[10:13] = [1] * 3
		tb[26:29] = [1] * 3
		self.assertEqual(new_board, tb)

	def test_char_recognizer(self):
		self.assertEqual(char_recognizer('*'), 0)
		self.assertEqual(char_recognizer('X'), 1)
		self.assertEqual(char_recognizer('O'),-1)
		self.assertEqual(char_recognizer('a'),-1)

	def test_asta_dikpala(self):
		board = [0] * 64
                board[27:29] = [1,-1]
                board[35:39] = [-1,1,1,1]
                board[20] = -1
                board[12] = -1
 		results1 = asta_dikpala(38,board,[0,4,4])
 		results2 = asta_dikpala(37,board,[0,4,4])
 		results3 = asta_dikpala(36,board,[0,4,4])
 		results4 = asta_dikpala(35,board,[0,4,4])
 		results5 = asta_dikpala(27,board,[0,4,4])
 		results6 = asta_dikpala(28,board,[0,4,4])
 		results7 = asta_dikpala(20,board,[0,4,4])
 		results8 = asta_dikpala(12,board,[0,4,4])

		board1 = board[:]
		board2 = board[:]
		board2[28] = 1
		board2[19] = 1
		board31 = board[:]
		board32 = board[:]
		board31[34:36] = [1,1]
		board32[28] = 1
		board32[20] = 1
		board32[12] = 1
		board32[4] = 1
		board41 = board[:]
		board41[36:40] = [-1] * 4
		board42 = board[:]
		board42[27] = -1
		board42[19] = -1
		board51 = board[:]
		board51[28:30] = [1] * 2
		board52 = board[:]
		board52[35] = 1
		board52[43] = 1
		board53 = board[:]
		board53[20] = 1
		board53[13] = 1
		board61 = board[:]
		board62 = board[:]
		board63 = board[:]
		board61[26:28] = [-1] * 2
		board62[36] = -1
		board62[44] = -1
		board63[37] = -1
		board63[46] = -1
		board7 = board[:]
		board7[27] = -1
		board7[34] = -1
		board8 = board[:]
		
		self.assertEqual(results1,[])
		self.assertEqual(results2,[(board2,19,[0,6,3])])
		self.assertEqual(results3,[(board32,4,[0,8,1]), (board31,34,[0,6,3])])
		self.assertEqual(results4,[(board42,19,[0,3,6]), (board41,39,[0,1,8])])
		self.assertEqual(results5,[(board52,43,[0,6,3]), (board51, 29,[0,6,3]), (board53,13,[0,6,3])])
		self.assertEqual(results6,[(board62,44,[0,3,6]), (board61,26,[0,3,6]), (board63,46,[0,3,6])])
		self.assertEqual(results7,[(board7, 34,[0,3,6])])
		self.assertEqual(results8,[])


		actions_x = action_results_generator((board, 0, [0, 4, 4]), 1)
		actions_o = action_results_generator((board, 0, [0, 4, 4]), -1)

		actions_dx = action_results_generator((board, 7, [0, 4, 4]), -1)
		actions_dx2 = action_results_generator((board, 4, [0, 4, 4]), 1)

		actions_do = action_results_generator((board, 5, [0, 4, 4]), 1)
		actions_do2 = action_results_generator((board, 10, [0, 4, 4]), -1)
		
		results3.extend(results5)
		results2.extend(results3)
		results1.extend(results2)

		results7.extend(results8)
		results6.extend(results7)
		results4.extend(results6)
		actions_tx = sorted(results1, key= lambda x: x[1])
		actions_to = sorted(results4, key=lambda x: x[1])

		self.assertEqual(actions_x, actions_tx)
		self.assertEqual(actions_dx, actions_tx)
		self.assertEqual(actions_dx2, actions_tx)

		self.assertEqual(actions_o, actions_to)
		self.assertEqual(actions_do, actions_to)
		self.assertEqual(actions_do2, actions_to)
		
		dead_end = [0] * 64
		dead_end[33:38] = [1] * 5
		actions_passx = action_results_generator((dead_end, 0, [0,5,0]), 1)	
		actions_passo = action_results_generator((dead_end, 0, [0,5,0]), -1)
		
		self.assertEqual(actions_passx,[(dead_end, "pass", [0,5,0])])
		self.assertEqual(actions_passo,[(dead_end, "pass", [0,5,0])])


		#eval_function testing
		self.assertEqual(eval_board((dead_end, 0, [0,5,0]), 1), 5)
		self.assertEqual(eval_board((board,0,[0,5,0]), 1),0)
		self.assertEqual(eval_board((board32,0,[0,5,0]), 1),8)
		self.assertEqual(eval_board((board32,3,[0,5,0]), 1),8)
		self.assertEqual(eval_board((board32,0,[0,5,0]), -1),-8)
		self.assertEqual(eval_board((board32,3,[0,5,0]), -1),-8)
		
	def test_read_input_file(self):
		t1 = read_input_txt_file("inputs/input1.txt")
		t2 = read_input_txt_file("inputs/input2.txt")
		t3 = read_input_txt_file("inputs/input3.txt")
		t4 = read_input_txt_file("inputs/input4.txt")
		
		board1 = [0] * 64
		board1[27] = -1
		board1[28] =  1
		board1[35] =  1
		board1[36] = -1
		board2 = board1[:]
		board2[0:4] = [-1] * 4
		board2[51:55] = [1] * 4
		self.assertEqual(t1, (1,1,1,(board1,0,[60,2,2])))
		self.assertEqual(t2, (2,-1,3,(board1,0,[60,2,2])))
		self.assertEqual(t3, (3,1,8,(board1,0,[60,2,2])))
		self.assertEqual(t4, (4,-1,1,(board2,0,[52,6,6])))
	
	def test_terminal_cutoff_test(self):
		log_data = []
		t1 = read_input_txt_file("inputs/input_cutoff.txt")
		t2 = read_input_txt_file("inputs/input2.txt")
		self.assertTrue(terminal_cutoff_test(t1[3], t1[1], t1[2], log_data))
		self.assertFalse(terminal_cutoff_test(t2[3], t1[1], t2[2], log_data))
		self.assertTrue(terminal_cutoff_test((t2[3][0],3,t2[3][2]), t2[1], t2[2], log_data))
		self.assertTrue(terminal_cutoff_test((t2[3][0],5,t2[3][2]), t2[1], t2[2], log_data))

	def test_board_print(self):
		file_handle = open("inputs/input1.txt",'r')
		task = int(file_handle.readline().rstrip())
        	player_string = file_handle.readline().rstrip()
        	cutoff_depth = int(file_handle.readline().rstrip())
		raw_read = []
		for x in range(0,8):
			raw_read.append(file_handle.readline().rstrip())

		t2 = read_input_txt_file("inputs/input2.txt")
		board_strings = board_print_string(t2[3][0])
		self.assertEqual(raw_read, board_strings)

	def test_resolve_node_inf_names(self):
		self.assertEqual(resolve_nodename(10),"c2")
		self.assertEqual(resolve_nodename("root"),"root")
		self.assertEqual(resolve_nodename("pass"),"pass")
		self.assertEqual(print_inf(10),"10")
		self.assertEqual(print_inf(-100),"-100")
		self.assertEqual(print_inf(64*99),"Infinity")
		self.assertEqual(print_inf(-1*64*99),"-Infinity")

	def test_max_min_cutoff_value(self):
		log_data = []
		t1 = read_input_txt_file("inputs/input_cutoff.txt")
		choice = max_value((t1[3][0],t1[3][1],t1[3][2],"root"), ninf, inf, t1[0], t1[1], t1[2],log_data)
		self.assertEqual(choice,((t1[3][0],t1[3][1],t1[3][2],"root"),12))
		#self.assertEqual(log_data,[("root",0,12,ninf,inf)])
		choice = min_value((t1[3][0],t1[3][1],t1[3][2],"root"), ninf, inf, t1[0], t1[1], t1[2], log_data)
		self.assertEqual(choice,((t1[3][0],t1[3][1],t1[3][2],"root"),12))
		#self.assertEqual(log_data,[("root",0,12,ninf,inf), ("root",0,12,ninf,inf)])

	def test_assignment_mode(self):
		t1 = read_input_txt_file("inputs/input_op_test1.txt")
		t2 = read_input_txt_file("inputs/input_op_test2.txt")
		t3 = read_input_txt_file("inputs/input_op_test3.txt")
		e1 = ["********","********","********","***XX***","****XX**","***XX***","********","********"]
		e2 = e1[:]
		e2.extend(["Node,Depth,Value","root,0,12"])
		e3 = e1[:]
		e3.extend(["Node,Depth,Value,Alpha,Beta","root,0,12,-Infinity,Infinity"])

		assignment_mode(*t1)
		file_handle = open("output.txt","r")
		check = []
		for x in range(0,8):
			check.append(file_handle.readline().rstrip())
		file_handle.close()
		self.assertEqual(check, e1)

		assignment_mode(*t2)
		file_handle = open("output.txt","r")
		check = []
		for x in range(0,10):
			check.append(file_handle.readline().rstrip())
		file_handle.close()
		self.assertEqual(check, e2)

		assignment_mode(*t3)
		file_handle = open("output.txt","r")
		check = []
		for x in range(0,10):
			check.append(file_handle.readline().rstrip())
		file_handle.close()
		self.assertEqual(check, e3)
		
	def test_min_max_recursive(self):
		t1 = read_input_txt_file("inputs/input_all.txt")
		assignment_mode(*t1)
		f1 = open("output.txt","r")
		f2 = open("inputs/output_all_3.txt","r")
		for x in range(0,42):
			self.assertEqual(f1.readline().rstrip(),f2.readline().rstrip())
		f1.close()
		f2.close()

if __name__ == '__main__':
    unittest.main()
