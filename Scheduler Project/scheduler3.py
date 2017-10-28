#!/usr/bin/env python
import sys
import time
import random
from queue import *

VERBOSE_FLAG = False; 

#create a process class and plug in the information for it
class Process:

	index = 0
	cpu_burst = 0
	i_o_burst = 0 
	finishing_time = 0
	turn_around_time = 0
	input_output_time = 0
	waiting_time = 0
	current_state = 'unstarted'
	ready_time = 0
	added = False

	def __init__(self, arrival_time, b_value, cpu_time, multiplier):
		self.arrival_time = arrival_time
		self.b_value = b_value
		self.cpu_time = cpu_time
		self.original_cpu_time = cpu_time #use this for printing 
		self.multiplier = multiplier
		

	def toString(self):
		return "("+str(self.arrival_time) + " " + str(self.b_value) + " " + str(self.original_cpu_time) + " " + str(self.multiplier)+")"

	def summary(self):
		print("Process "+ str(self.index))
		print("\t(A,B,C,M) = "+self.toString())
		print("\tFinishing Time: " + str(self.finishing_time))
		print("\tTurnaround time: "+ str(self.finishing_time - self.arrival_time))
		print("\tI/O time: "+ str(self.input_output_time))
		print("\tWaiting time: "+ str(self.waiting_time))


#create the randomOS method
def randomOS(U):

	#open the random-numbers file
	random_file = open("random-numbers.txt","r")

	#figure out the number of lines in the file
	num_lines = sum(1 for line in random_file)

	rand_index = random.randint(1,num_lines)

	random_file = open("random-numbers.txt","r")

	#now get some random number from the file
	random_number = random_file.read().splitlines()[rand_index]


	random_number = [int(s) for s in random_number.split() if s.isdigit()]

	return_val = 1 + (random_number[0] % U)

	return return_val


#print out the verbose requirements 
def verbose_function(process_array,cycle):
	cycle_string = "Before cycle " + str(cycle) + ":    "
	for i in range(0, len(process_array)):
		cycle_string += process_array[i].current_state + " " 

		if(process_array[i].current_state == "running"):
			cycle_string += str(process_array[i].cpu_burst) + "  "

		elif(process_array[i].current_state == "blocked"):
			cycle_string += str(process_array[i].i_o_burst) + "  "

		else:
			cycle_string += "0 "

	print(cycle_string)	


def full_summary(process_array,num_process):

	max_end_time = 0
	cpu_total = 0
	i_o_total = 0
	throughput_total = 0
	total_turnaround = 0
	total_wait = 0

	if(len(process_array) > 1):

		for i in range(0,len(process_array)):
			if(process_array[i].finishing_time > max_end_time):
				max_end_time = process_array[i].finishing_time

			if(process_array[i].finishing_time < 100):
				throughput_total += 1

			cpu_total += process_array[i].original_cpu_time
			i_o_total += process_array[i].input_output_time
			total_turnaround += process_array[i].turn_around_time
			total_wait += process_array[i].waiting_time
	else:
		cpu_total += process_array[0].original_cpu_time
		i_o_total += process_array[0].input_output_time
		total_turnaround += process_array[0].turn_around_time
		total_wait += process_array[0].waiting_time
		max_end_time = process_array[0].finishing_time

		if(process_array[0].finishing_time < 100):
			throughput_total += 1


	cpu_util = cpu_total/max_end_time
	i_o_util = i_o_total/max_end_time
	throughput_total = 100/max_end_time
	avg_turn = total_turnaround/num_process
	avg_wait = total_wait/num_process

	print("")
	print("Summary Data:")
	print("\tFinishing Time: "+str(max_end_time))
	print("\tCPU Utilization: " + str(cpu_util))
	print("\tI/O Utilization: "+ str(i_o_util))
	print("\tThroughput: "+ str(throughput_total*num_process))
	print("\tAverage turnaround time: "+ str(avg_turn))
	print("\tAverage waiting time: "+ str(avg_wait))









#check to see if the verbose flag was used and 
#read in the file for the process information
if(len(sys.argv) == 3):
	VERBOSE_FLAG = True; 
	process_file = open(sys.argv[2])

else:
	process_file = open(sys.argv[1])


#get the number of processes
num_process = int(process_file.read(1))

#this is where we get the single first line that contains the information
#this will be a single string
process_line = process_file.readline()

#break down the process_list string into an array that contains an array of ints
#that represent the information for each process
process_nums = [int(s) for s in process_line.split() if s.isdigit()]

#in the case there are more than one process use the while loop
#otherwise it isn't neccesary

#now create an array of processes with the information provided by process_list
process_array = []

if(process_nums != 1):

	process_list = []
	temp_array = []

	#now divide each set of numbers into their respective process
	process_count = 0
	index = 0

	#this while loop simply split the array up and puts them into individual arrays for later
	#conversion to processes
	while(process_count < num_process):

		

		temp_array.append(process_nums[index])

		index += 1

		if((index % 4) == 0):
			process_count += 1
			process_list.append(temp_array)
			temp_array = []

	for i in range(0, len(process_list)):

		#dont do the randomOS function here because you recalculate that every cycle
		process = Process(int(process_list[i][0]),int(process_list[i][1]),int(process_list[i][2]),int(process_list[i][3]))

		process_array.append(process)

else:
	process_array.append(Process(int(process_nums[0]),int(process_list[1]),int(process_nums[2]),int(process_nums[3])))



#sort the array by checking arrival times
def bubble_sort_arrival(arr):
    check = True
    while check:
        check = False
        for i in range(0,len(arr)-1):
            if arr[i].arrival_time > arr[i+1].arrival_time:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                check = True

#print out the initial heading have to convert the array into a string
header_string = "The original input was: " + str(num_process) + " "

for i in range(0,len(process_array)):
	header_string += process_array[i].toString() + " "

header_string += "\n" + "The sorted input is: " + str(num_process) + " "

bubble_sort_arrival(process_array)

#now set the index of each process later so that we can properly print out their details and keep track of them
for i in range(0,len(process_array)):
	process_array[i].index = i

for i in range(0,len(process_array)):
	header_string += process_array[i].toString() + " "

print(header_string)
print()



def first_in_first_out(process_array):

	terminated_array = []

	ready_array = []

	blocked_array = []

	ready_array.append(process_array[0])
	process_array[0].added = True

	cycle = 0

	if(VERBOSE_FLAG):
	print("This detailed printout gives the state and remaining burst for each process")
	print()

	for i in range(1,len(process_array)):

		ready_array.append(process_array[i])
		process_array[i].added = True
		process_array[i].current_state = "ready"


	terminated_processes = 0

	while(terminated_processes != len(process_array)):

		while((len(ready_array) == 0) == False):

			process = ready_array.pop()

			process.current_state = "running"

			process.cpu_burst = randomOS(process.b_value)

			if(process.cpu_burst > process.cpu_time):
				process.cpu_burst = process.cpu_time

			process.cpu_time -= burst

			for i in range(0,len(ready_array)):

					process_array[i].current_state == "ready"
					process_array[i].waiting_time += process.cpu_burst
					process_array[i].finishing_time += process.cpu_burst

			block_remove = []

			for i in range(0,len(blocked_array)):

				if(blocked_array[i].i_o_burst <= process.cpu_burst):

					blocked_array[i].finishing_time += process.cpu_burst
					blocked_array[i].waiting_time += process.cpu_burst - blocked_array[i].i_o_burst
					blocked_array[i].i_o_burst = 0
					block_remove.append(blocked_array[i])
					ready.append(blocked_array[i])
					blocked_array[i].current_state = "ready"

				else:

					blocked_array[i].i_o_burst -= process.cpu_burst
					blocked_array[i].finishing_time += process.cpu_burst

					blocked_array[i].current_state = "blocked"

			for i in range(0,len(block_remove)):

				blocked_array.remove(block_remove[i])


			for 








first_in_first_out(process_array)