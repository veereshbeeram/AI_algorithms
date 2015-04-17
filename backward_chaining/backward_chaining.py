#!/usr/bin/python

import sys
import re
import copy

class KBase:
	''' The Knowledge base class.
	    Contains all DS & methods to build & use a full KB.
		It will contain a List of sentences.
		It will contain a inverted index on those sentences, so that we can identify unifyable sentences fast.
		Also contains a method: fetch_rules_for_goal(sentence)
	'''
	def __init__(self):
		''' constructor initializing the members '''
		self.KB = [] 
		self.sentence_index = dict([("1", dict()),("2", dict())])

	def append_kb(self,sentence):
		''' add the given sentence at the end of KB'''
		self.insert_at(sentence,len(self.KB))

	def insert_at(self,sentence, index):
		''' insert the sentence at given index in KB '''
		sentence_object = Sentence(sentence)
		self.KB.insert(index, sentence_object)
		target_dict = self.sentence_index[str(sentence_object.RHS.numargs)]
		if(target_dict.get(sentence_object.RHS.name)):
			target_dict[sentence_object.RHS.name].append(index)
		else:
			target_dict[sentence_object.RHS.name] = [index]

	def fetch_rules_for_goal(self,goal):
		''' return list of sentences that can unify with the input predicate'''
		target_dict = self.sentence_index[str(goal.numargs)]
		goal_list = []
		if(target_dict.get(goal.name)):
			index_list = target_dict[goal.name]
			goal_list
			for i in index_list:
				goal_list.append(self.KB[i])
		return goal_list

	def extend_kb(self,list_sentences):
		''' extend the KB by appending each of the list_sentences '''
		for sentence in list_sentences:
			self.append_kb(sentence)

	def to_string(self):
		''' a helper method to dump the KB in a human readable format '''
		sentence_strings = [] 
		for x in self.KB:
			sentence_strings.append(x.to_string())
		return (sentence_strings, self.sentence_index)

class Sentence:
	''' defines a sentence as a LHS & RHS for Horn clauses.
		
	'''
	horn_pattern = re.compile(r'(.*)=>(.*)')
	lhs_split_pattern = re.compile(r'\&')
	def __init__(self,sentence_string):
		self.RHS = None
		self.LHS = [] 
		self.convert_to_sentence(sentence_string)

	def is_atomic(self,sentence_string):
		''' tells you if it is a atomic sentence'''
		if(self.horn_pattern.match(sentence_string)):
			return False 
		else:
			return True

	def split_horn_string(self,sentence_string):
		''' splits string at => into 2 '''
		return self.horn_pattern.match(sentence_string).groups()		

	def make_lhs(self,lhs_sentence_string):
		''' splits the and's & makes a list out of each predicate '''
		lhs_predicates = self.lhs_split_pattern.split(lhs_sentence_string)
		for predicate in lhs_predicates:
			self.LHS.append(Predicate(predicate))

	def convert_to_sentence(self,sentence_string):
		''' convert the string to a sentence & return the sentence'''
		if(self.is_atomic(sentence_string)):
			self.RHS = Predicate(sentence_string)
		else:
			lhs_string,rhs_string = self.split_horn_string(sentence_string)
			self.RHS = Predicate(rhs_string)
			self.make_lhs(lhs_string)

	def to_string(self):
		''' helper class to visualize sentence object '''
		lhs_strings = [] 
		for lhs in self.LHS:
			lhs_strings.append(lhs.to_string())
		rhs_strings = self.RHS.to_string()
		return (lhs_strings, rhs_strings)

class Predicate:
	''' defines the structre of a predicate '''
	one_arg_pattern = re.compile(r"^\s*(\w+)\s*\(\s*(\w+)\s*\)\s*$")
	two_arg_pattern = re.compile(r"^\s*(\w+)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*$")
	def __init__(self,predicate_string):
		self.name = ""
		self.numargs = 0
		self.arg1 = ""
		self.arg2 = ""
		self.make_predicate(predicate_string)

	def make_predicate(self,predicate_string):
		''' given a string, populate the predicate'''
		matching = self.one_arg_pattern.match(predicate_string)
		if(matching):
			self.numargs = 1
			self.name, self.arg1 = matching.groups()
		else:
			matching = self.two_arg_pattern.match(predicate_string)
			if(matching):
				self.numargs = 2
				self.name, self.arg1, self.arg2 = matching.groups()

	def substitute(self,theta):
		''' substitute theta into this predicate
			return substituted predicate  '''
		new_predicate = copy.copy(self) 
		if(theta == ""):
			return new_predicate
		if(new_predicate.arg1 == "x"):
			new_predicate.arg1 = theta
		if(new_predicate.numargs == 2 and new_predicate.arg2 == "x"):
			new_predicate.arg2 = theta
		return new_predicate

	def simple_unify(self,goal_predicate, theta):
		''' self is the RHS of some sentence, goal_predicate is the goal with which we wish to unify '''
		if(self.numargs != goal_predicate.numargs):
			return None
		if(self.arg1 != "x" and goal_predicate.arg1 != "x" and self.arg1 != goal_predicate.arg1):
			return None
		if(self.numargs == 2 and self.arg2 != "x" and goal_predicate.arg2 != "x" and self.arg2 != goal_predicate.arg2):
			return None
		if(self.arg1 == "x" and goal_predicate.arg1 != "x" and theta != "" and theta != None and theta != goal_predicate.arg1):
			return None
		if(self.arg2 == "x" and goal_predicate.arg2 != "x" and theta != "" and theta != None and theta != goal_predicate.arg2 and self.numargs==2):
			return None
		if(self.arg1 == "x" and goal_predicate.arg1 != "x"):
			return goal_predicate.arg1
		if(self.numargs==2 and self.arg2 == "x" and goal_predicate.arg2 != "x"):
			return goal_predicate.arg2
		if(self.arg1 != "x" and goal_predicate.arg1 == "x" and theta != "" and theta != None and theta != self.arg1):
			return None
		if(self.arg2 != "x" and goal_predicate.arg2 == "x" and theta != "" and theta != None and theta != self.arg2 and self.numargs==2):
			return None
		if(self.arg1 != "x" and goal_predicate.arg1 == "x"):
			return self.arg1
		if(self.numargs==2 and self.arg2 != "x" and goal_predicate.arg2 == "x"):
			return self.arg2
		if(self.arg1 == goal_predicate.arg1  and self.numargs==1):
			return theta
		if(self.arg1 == goal_predicate.arg1 and self.numargs==2 and self.arg2 == goal_predicate.arg2):
			return theta
		return ""

	def to_string(self):
		return (self.name,self.numargs,self.arg1,self.arg2)

def read_input_txt_hw3_file(filename):
	''' Given a input file of assumed format, read & populate the KB'''
	r_file_handle = open(filename,"r") #TODO error handling
	query_string = r_file_handle.readline().rstrip()
	num_sentences = int(r_file_handle.readline().rstrip())
	sentence_string = [] 
	for x in range(0,num_sentences):
		sentence_string.append( r_file_handle.readline().rstrip())
	KB = KBase()
	KB.extend_kb(sentence_string)
	query = Predicate(query_string)
	return KB,query


def backward_chaining(KB,query):
	''' do backward chaining & return true or false
		This is FOL-BC-ASK
	'''
	theta_list = fol_bc_or(KB,query,"")
	#print theta_list
	if(len(theta_list)>0):
		return True
	else:
		return False

def fol_bc_or(KB,goal,theta):
	''' return  actual subsitutions'''
	#print "OR " +str(goal.to_string()) + " " + theta
	goal_rules = KB.fetch_rules_for_goal(goal)
	theta_or = [] 
	for sentence in goal_rules:
		theta_or.extend( fol_bc_and(KB,sentence.LHS,sentence.RHS.simple_unify(goal,theta)) )
	#print "ORret: "+str(theta_or)
	return theta_or


def fol_bc_and(KB,goals,theta):
	''' return suitable substitutions '''
	#print "AND: "+ str(theta)
	#for goal in goals:
		#print goal.to_string()
	theta_and = [] 
	if(theta != None):
		if(len(goals) == 0):
			#print "ANDret: "+str([theta])
			return [theta] 
		else:
			f_predicate = goals.pop(0)
			for t in fol_bc_or(KB,f_predicate.substitute(theta),theta):
				for t2 in fol_bc_and(KB,goals[:],t):
					theta_and.append(t2)
		#print "ANDret: "+str(theta_and)
		return theta_and
	else:
		#print "ANDret: "+str([])
		return [] 

def write_output_to(answer,filename):
	w_file_handle = open(filename,"w")
	if(answer):
		w_file_handle.write("TRUE\n")
	else:
		w_file_handle.write("FALSE\n")
	w_file_handle.close()

if __name__ == "__main__":
        KB,query = read_input_txt_hw3_file("input.txt")
	answer = backward_chaining(KB,query)
	write_output_to(answer,"output.txt")
