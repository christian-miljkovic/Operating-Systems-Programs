#!/usr/bin/env python
import sys
import time
import random
from queue import *
import pdb 

VERBOSE_FLAG = False; 

#create a process class and plug in the information for it
class Process:

	index = 0
	original_cpu_burst = 0
	cpu_burst = 0
	i_o_burst = 0 
	finishing_time = 0
	turn_around_time = 0
	input_output_time = 0
	waiting_time = 0
	current_state = 'unstarted'
	ready_time = 0
	time_waited = 0
	

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

if(VERBOSE_FLAG):
	print("This detailed printout gives the state and remaining burst for each process")
	print()



def first_in_first_out(process_array):

	all_terminated = False

	

	#index = 0 means running, index > 0 means ready, not within the queue means blocked
	process_queue = []

	blocking_list = []

	unstarted_list = []

	cycle = 0
	

	while(all_terminated == False):

		check_sum = 0

		if(VERBOSE_FLAG):
			verbose_function(process_array,cycle)

		#pdb.set_trace()
		
		#this is the initial check getting processes from state: unstarted to ready or running
		for i in range(0,len(process_array)):


			if((process_array[i].current_state == "unstarted") and (process_array[i].arrival_time == 0)):

				#we want to add it only if we wont be adding something before from previous runs
				process_queue.append(process_array[i])	

			elif((process_array[i].current_state == "unstarted") and (process_array[i].arrival_time == cycle) and (cycle > 0)):

				#wait until the end to add it so we can make changes
				unstarted_list.append(process_array[i])

			#will need to check to put back into process_queue when its unblocked

		#now go through the loop and update processes based on their positions #using the "queue" array

		if(len(process_queue) > 0):

			make_pop = False
			pop_array = []


			for i in range(0,len(process_queue)):


				#check if has been set to running yet if it is unstarted or a first arrived ready process
				if(((process_queue[i].current_state == "unstarted") or (process_queue[i].current_state == "ready") or (process_queue[i].current_state == "blocked")) and (i == 0)):

					process_queue[i].current_state = "running"


					#compute the cpu burst
					#calculate the randomOS time for the single burst
					process_queue[i].cpu_burst = randomOS(process_queue[i].b_value)

					#if the burst is greater than the cpu time left set it equal to that
					if(process_queue[i].cpu_burst > process_queue[i].cpu_time):
						process_queue[i].cpu_burst = process_queue[i].cpu_time

					#calcualte the I/O burst
					process_queue[i].i_o_burst = process_queue[i].cpu_burst * process_queue[i].multiplier

				elif((process_queue[i].current_state == "blocked") and (i >0)):

					if(process_queue[i].i_o_burst == 1):
						process_queue[i].i_o_burst -= 1

					if(process_queue[0].current_state == "terminated" or process_queue[0].current_state == "blocked" and i==1):
						process_queue[i].current_state = "running"

					else:
						process_queue[i].current_state = "ready"


				#if the first index process is running then we compute how much more is it running for
				elif((process_queue[i].current_state == "running") and (i == 0)):

					if(process_queue[i].cpu_burst > 0):
						process_queue[i].cpu_burst -= 1

					if(process_queue[i].cpu_time > 0):
						process_queue[i].cpu_time -= 1



					#now figure out whether to turn into blocked process or terminated else keep running and same position
					if((process_queue[i].cpu_burst == 0) and (process_queue[i].cpu_time == 0)):
						
						process_queue[i].current_state = "terminated"
						process_queue[i].finishing_time = cycle
						process_queue[i].turn_around_time = process_queue[i].finishing_time - process_queue[i].arrival_time
						#now pop the process because we are done with running it
						pop_array.append(process_queue[i])

					#now we are blocking the process
					elif((process_queue[i].cpu_burst == 0) and (process_queue[i].cpu_time > 0)):
						process_queue[i].current_state = "blocked"
						pop_array.append(process_queue[i])


					#we keep it running
					#else:


				#we are not checking for terminated because it should not be in here
				elif((i > 0) and ((process_queue[i].current_state =="blocked") or (process_queue[i].current_state =="unstarted")) and ((process_queue[0].current_state !="blocked"))):
					
					#print(process_queue[i].toString(),process_queue[i].current_state)
					process_queue[i].current_state = "ready"


				#if we havent popped the done process in first index we change the next process behind it to running
				#assuming that the previous run we have index 0 running and index 1 had been changed to ready
				elif((len(process_queue) > 1) and ((process_queue[0].current_state =="blocked") or (process_queue[0].current_state =="terminated"))):

					if(process_queue[0].index != process_queue[1].index):
						process_queue[1].current_state = "running"

						
						#compute the cpu burst
						#calculate the randomOS time for the single burst
						process_queue[1].cpu_burst = randomOS(process_queue[1].b_value)

						#if the burst is greater than the cpu time left set it equal to that
						if(process_queue[1].cpu_burst > process_queue[1].cpu_time):
							process_queue[1].cpu_burst = process_queue[1].cpu_time


						#calcualte the I/O burst
						process_queue[1].i_o_burst = process_queue[1].cpu_burst * process_queue[1].multiplier


			temp_array = []

			if(len(pop_array) > 0):
				# save this for later blocking_list.append(process_queue.pop(0))
				for i in range(0,len(pop_array)):

					if(pop_array[i].current_state == "terminated"):
						process_queue.remove(pop_array[i])
					else:
						temp_array.append(pop_array[i])
						process_queue.remove(pop_array[i])
				pop_array = []

			
			#if it is turned to blocking above it will then set this
			#update any blocked processes
			if(len(blocking_list) > 0):

				removal_list = []

				for i in range(0,len(blocking_list)):


					####################################
					#This is where i think the problem is 
					######################################

					#if it is done with i/o then put it back on the queue
					if(blocking_list[i].i_o_burst == 1):
						

						

						#now we determine if its going to be running or ready
						if(len(process_queue) == 0):

							#pdb.set_trace()

							if(blocking_list[i].time_waited > 0):

								#problem here is if it just got blocked
								blocking_list[i].current_state = "running"
								blocking_list[i].time_waited = 0
								

								#compute the cpu burst
								#calculate the randomOS time for the single burst
								blocking_list[i].cpu_burst = randomOS(blocking_list[i].b_value)

								#if the burst is greater than the cpu time left set it equal to that
								if(blocking_list[i].cpu_burst > blocking_list[i].cpu_time):
									blocking_list[i].cpu_burst = blocking_list[i].cpu_time

								#calcualte the I/O burst
								blocking_list[i].i_o_burst = blocking_list[i].cpu_burst * blocking_list[i].multiplier

								process_queue.append(blocking_list[i])
								removal_list.append(blocking_list[i])

							else:
								blocking_list[i].time_waited += 1



								

						#otherwise we know that it isn't the first
						else:

							if(blocking_list[i].time_waited > 0):

								#check if the current process that is first on the index is blocked or terminated and just hasnt been popped yet
								if((process_queue[0].current_state == "terminated") or (process_queue[0].current_state == "blocked") and (i>0)):
									
									blocking_list[i].current_state = "running"
									blocking_list[i].time_waited = 0
									
									#compute the cpu burst
									#calculate the randomOS time for the single burst
									blocking_list[i].cpu_burst = randomOS(blocking_list[i].b_value)

									#if the burst is greater than the cpu time left set it equal to that
									if(blocking_list[i].cpu_burst > blocking_list[i].cpu_time):
										blocking_list[i].cpu_burst = blocking_list[i].cpu_time


									#calcualte the I/O burst
									blocking_list[i].i_o_burst = blocking_list[i].cpu_burst * blocking_list[i].multiplier
									process_queue.append(blocking_list[i])
									removal_list.append(blocking_list[i])
									


								elif((process_queue[0].current_state == "running")):

									##try making it so that if you know that it is a smaller index and only has 1 cpu burst left
									blocking_list[i].current_state = "ready"
									blocking_list[i].time_waited = 0

									process_queue.append(blocking_list[i])
									removal_list.append(blocking_list[i])
							else:
								blocking_list[i].time_waited += 1
								
					

					#otherwise it is not done blocking
					else:
						blocking_list[i].i_o_burst -= 1
						blocking_list[i].time_waited += 1

				for i in range(0,len(removal_list)):
					blocking_list.remove(removal_list[i])	
			
		#this is if there are no more process ready or running
		elif(len(process_queue)==0):

			removal_list2 = []

			for i in range(0,len(process_array)):

				if(process_array[i].current_state == "blocked"):

					#calculate the i_o time left

					#if it is done with i/o then put it back on the queue
					if(process_array[i].i_o_burst == 1):
						process_array[i].i_o_burst -= 1

						if(process_array[i].cpu_time > 0):
						

							#now we determine if its going to be running or ready be careful because since we have an array
							#within this for loop we could have added to the queue
							if(len(process_queue) == 0):

								#if it is the first one to be on the ready queue then we compute all the neccesary parameters
								#problem is here where if if just got blocked
								process_array[i].current_state = "running"
								


								#compute the cpu burst
								#calculate the randomOS time for the single burst
								process_array[i].cpu_burst = randomOS(process_array[i].b_value)

								#if the burst is greater than the cpu time left set it equal to that
								if(process_array[i].cpu_burst > process_array[i].cpu_time):
									process_array[i].cpu_burst = process_array[i].cpu_time

								#calcualte the I/O burst
								process_array[i].i_o_burst = process_array[i].cpu_burst * process_array[i].multiplier

								process_queue.append(process_array[i])
								removal_list2.append(process_array[i])


							#otherwise we know that it isn't the first
							else:
								process_array[i].current_state = "ready"
								process_queue.append(process_array[i])
								removal_list2.append(process_array[i])

						#we know that cpu time isnt done
						else:
							process_array[i].current_state = "terminated"


					#otherwise it is not done blocking
					else:
						process_array[i].i_o_burst -= 1

			for i in range(0,len(removal_list2)):
				blocking_list.remove(removal_list2[i])

		
		if(len(unstarted_list) > 0):

			for i in range(0,len(unstarted_list)):

				make_run = True
				removal_list_unstarted = []

				for j in range(0,len(process_queue)):

					if(process_queue[j].current_state == "running"):
						make_run = False

				if(make_run):
					unstarted_list[i].current_state = "running"
					#compute the cpu burst
					#calculate the randomOS time for the single burst
					unstarted_list[i].cpu_burst = randomOS(unstarted_list[i].b_value)

					#if the burst is greater than the cpu time left set it equal to that
					if(unstarted_list[i].cpu_burst > unstarted_list[i].cpu_time):
						unstarted_list[i].cpu_burst = unstarted_list[i].cpu_time

					#calcualte the I/O burst
					unstarted_list[i].i_o_burst = unstarted_list[i].cpu_burst * unstarted_list[i].multiplier

					process_queue.append(unstarted_list[i])
					removal_list_unstarted.append(unstarted_list[i])


				else:
					unstarted_list[i].current_state = "ready"
					process_queue.append(unstarted_list[i])
					removal_list_unstarted.append(unstarted_list[i])

			for i in range(0,len(removal_list_unstarted)):
				unstarted_list.remove(removal_list_unstarted[i])

		if(len(temp_array) > 0):
			for i in range(0,len(temp_array)):
				if(temp_array[i].current_state == "blocked"):
					temp_array[i].time_waited += 1
					blocking_list.append(temp_array[i])
					temp_array.remove(temp_array[i])
			
		#check if the processes are terminated
		for i in range(0,len(process_array)):
			if(process_array[i].current_state == "terminated"):
				check_sum += 1

		
		#check to see if everything is terminated
		if(check_sum == num_process):
			all_terminated = True

		#update the waiting time, i/o time etc here after each cycle
		for i in range(0,len(process_array)):

			if(process_array[i].current_state == "blocked" and process_array[i].i_o_burst != 0):
				process_array[i].input_output_time += 1

			elif(process_array[i].current_state == "ready"):
				process_array[i].waiting_time += 1

		
		cycle += 1
		#pdb.set_trace()
	print("The scheduling algorithm used was First Come First Served")
	print("")
	for i in range(0,len(process_array)):
		process_array[i].summary()
	full_summary(process_array,num_process)



#first_in_first_out(process_array)

def round_robbin(process_array,quantum):

	all_terminated = False

	

	#index = 0 means running, index > 0 means ready, not within the queue means blocked
	process_queue = []

	blocking_list = []

	unstarted_list = []

	cycle = 0
	

	while(all_terminated == False):

		check_sum = 0

		if(VERBOSE_FLAG):
			verbose_function(process_array,cycle)

		#pdb.set_trace()
		
		#this is the initial check getting processes from state: unstarted to ready or running
		for i in range(0,len(process_array)):


			if((process_array[i].current_state == "unstarted") and (process_array[i].arrival_time == 0)):

				#we want to add it only if we wont be adding something before from previous runs
				process_queue.append(process_array[i])	

			elif((process_array[i].current_state == "unstarted") and (process_array[i].arrival_time == cycle) and (cycle > 0)):

				#wait until the end to add it so we can make changes
				unstarted_list.append(process_array[i])

			#will need to check to put back into process_queue when its unblocked

		#now go through the loop and update processes based on their positions #using the "queue" array

		if(len(process_queue) > 0):

			make_pop = False
			pop_array = []


			for i in range(0,len(process_queue)):


				#check if has been set to running yet if it is unstarted or a first arrived ready process
				if(((process_queue[i].current_state == "unstarted") or (process_queue[i].current_state == "ready") or (process_queue[i].current_state == "blocked")) and (i == 0)):

					process_queue[i].current_state = "running"


					#compute the cpu burst
					#calculate the randomOS time for the single burst
					process_queue[i].cpu_burst = randomOS(process_queue[i].b_value)
					process_queue[i].original_cpu_burst = process_queue[i].cpu_burst

					if(process_queue[i].cpu_burst > quantum):
						process_queue[i].cpu_burst = quantum

					#if the burst is greater than the cpu time left set it equal to that
					if(process_queue[i].cpu_burst > process_queue[i].cpu_time):
						process_queue[i].original_cpu_burst = process_queue[i].cpu_time

					#calcualte the I/O burst
					process_queue[i].i_o_burst = process_queue[i].original_cpu_burst * process_queue[i].multiplier

				elif((process_queue[i].current_state == "blocked") and (i >0)):

					if(process_queue[i].i_o_burst == 1):
						process_queue[i].i_o_burst -= 1

					if(process_queue[0].current_state == "terminated" or process_queue[0].current_state == "blocked" and i==1):
						process_queue[i].current_state = "running"

					else:
						process_queue[i].current_state = "ready"

				elif((process_queue[i].current_state == "running") and (i == 0) and (process_queue[i].cpu_burst < process_queue[i].original_cpu_burst)):

					if(process_queue[i].cpu_burst > 0):
						process_queue[i].cpu_burst -= 1
						process_queue[i].original_cpu_burst -= 1

					if(process_queue[i].cpu_time > 0):
						process_queue[i].cpu_time -= 1

					if((process_queue[i].original_cpu_burst == 0) and (process_queue[i].cpu_time == 0)):
						process_queue[i].current_state = "terminated"
						process_queue[i].finishing_time = cycle
						process_queue[i].turn_around_time = process_queue[i].finishing_time - process_queue[i].arrival_time
						#now pop the process because we are done with running it
						pop_array.append(process_queue[i])

					#prempt it here
					elif((process_queue[i].cpu_burst == 0) and (process_queue[i].original_cpu_burst > process_queue[i].cpu_burst)):
						process_queue[i].current_state = "ready"
						pop_array.append(process_queue[i])


				#if the first index process is running then we compute how much more is it running for
				elif((process_queue[i].current_state == "running") and (i == 0)):

					if(process_queue[i].cpu_burst > 0):
						process_queue[i].cpu_burst -= 1

					if(process_queue[i].cpu_time > 0):
						process_queue[i].cpu_time -= 1



					#now figure out whether to turn into blocked process or terminated else keep running and same position
					if((process_queue[i].cpu_burst == 0) and (process_queue[i].cpu_time == 0)):
						
						process_queue[i].current_state = "terminated"
						process_queue[i].finishing_time = cycle
						process_queue[i].turn_around_time = process_queue[i].finishing_time - process_queue[i].arrival_time
						#now pop the process because we are done with running it
						pop_array.append(process_queue[i])

					#now we are blocking the process
					elif((process_queue[i].cpu_burst == 0) and (process_queue[i].cpu_time > 0)):
						process_queue[i].current_state = "blocked"
						pop_array.append(process_queue[i])


					#we keep it running
					#else:


				#we are not checking for terminated because it should not be in here
				elif((i > 0) and ((process_queue[i].current_state =="blocked") or (process_queue[i].current_state =="unstarted")) and ((process_queue[0].current_state !="blocked"))):
					
					#print(process_queue[i].toString(),process_queue[i].current_state)
					process_queue[i].current_state = "ready"


				#if we havent popped the done process in first index we change the next process behind it to running
				#assuming that the previous run we have index 0 running and index 1 had been changed to ready
				elif((len(process_queue) > 1) and ((process_queue[0].current_state =="blocked") or (process_queue[0].current_state =="terminated") or (process_queue[0].current_state =="ready"))):

					if(process_queue[0].index != process_queue[1].index):
						process_queue[1].current_state = "running"

						
						#compute the cpu burst
						#calculate the randomOS time for the single burst
						process_queue[1].cpu_burst = randomOS(process_queue[1].b_value)
						process_queue[1].original_cpu_burst = process_queue[1].cpu_burst

						if(process_queue[1].cpu_burst > quantum):
							process_queue[1].cpu_burst = quantum						

						#if the burst is greater than the cpu time left set it equal to that
						if(process_queue[1].cpu_burst > process_queue[1].cpu_time):
							process_queue[1].original_cpu_burst = process_queue[1].cpu_time


						#calcualte the I/O burst
						process_queue[1].i_o_burst = process_queue[1].original_cpu_burst * process_queue[1].multiplier


			temp_array = []

			if(len(pop_array) > 0):
				# save this for later blocking_list.append(process_queue.pop(0))
				for i in range(0,len(pop_array)):

					if(pop_array[i].current_state == "terminated"):
						process_queue.remove(pop_array[i])

					elif(pop_array[i].current_state == "ready" and process_queue[0].index == pop_array[i].index):

						temp_process = process_queue.pop(0)
						process_queue.append(temp_process)

					else:
						temp_array.append(pop_array[i])
						process_queue.remove(pop_array[i])
				pop_array = []

			
			#if it is turned to blocking above it will then set this
			#update any blocked processes
			if(len(blocking_list) > 0):

				removal_list = []

				for i in range(0,len(blocking_list)):



					#if it is done with i/o then put it back on the queue
					if(blocking_list[i].i_o_burst == 1):
						
						#now we determine if its going to be running or ready
						if(len(process_queue) == 0):

							#pdb.set_trace()

							if(blocking_list[i].time_waited > 0):

								#problem here is if it just got blocked
								blocking_list[i].current_state = "running"
								blocking_list[i].time_waited = 0
								

								#compute the cpu burst
								#calculate the randomOS time for the single burst
								blocking_list[i].cpu_burst = randomOS(blocking_list[i].b_value)
								blocking_list[i].original_cpu_burst = blocking_list[i].cpu_burst

								if(blocking_list[i].cpu_burst > quantum):
									blocking_list[i].cpu_burst = quantum								

								#if the burst is greater than the cpu time left set it equal to that
								if(blocking_list[i].cpu_burst > blocking_list[i].cpu_time):
									blocking_list[i].original_cpu_burst = blocking_list[i].cpu_time

								#calcualte the I/O burst
								blocking_list[i].i_o_burst = blocking_list[i].original_cpu_burst * blocking_list[i].multiplier

								process_queue.append(blocking_list[i])
								removal_list.append(blocking_list[i])

							else:
								blocking_list[i].time_waited += 1



								

						#otherwise we know that it isn't the first
						else:

							if(blocking_list[i].time_waited > 0):

								#check if the current process that is first on the index is blocked or terminated and just hasnt been popped yet
								if((process_queue[0].current_state == "terminated") or (process_queue[0].current_state == "blocked") and (i>0)):
									
									blocking_list[i].current_state = "running"
									blocking_list[i].time_waited = 0
									
									#compute the cpu burst
									#calculate the randomOS time for the single burst
									blocking_list[i].cpu_burst = randomOS(blocking_list[i].b_value)
									blocking_list[i].original_cpu_burst = blocking_list[i].cpu_burst

									if(blocking_list[i].cpu_burst > quantum):
										blocking_list[i].cpu_burst = quantum									

									#if the burst is greater than the cpu time left set it equal to that
									if(blocking_list[i].cpu_burst > blocking_list[i].cpu_time):
										blocking_list[i].original_cpu_burst = blocking_list[i].cpu_time


									#calcualte the I/O burst
									blocking_list[i].i_o_burst = blocking_list[i].original_cpu_burst * blocking_list[i].multiplier
									process_queue.append(blocking_list[i])
									removal_list.append(blocking_list[i])
									


								elif((process_queue[0].current_state == "running")):

									##try making it so that if you know that it is a smaller index and only has 1 cpu burst left
									blocking_list[i].current_state = "ready"
									blocking_list[i].time_waited = 0

									process_queue.append(blocking_list[i])
									removal_list.append(blocking_list[i])
							else:
								blocking_list[i].time_waited += 1
								
					

					#otherwise it is not done blocking
					else:
						blocking_list[i].i_o_burst -= 1
						blocking_list[i].time_waited += 1

				for i in range(0,len(removal_list)):
					blocking_list.remove(removal_list[i])	
			
		#this is if there are no more process ready or running
		elif(len(process_queue)==0):

			removal_list2 = []

			for i in range(0,len(process_array)):

				if(process_array[i].current_state == "blocked"):

					#calculate the i_o time left

					#if it is done with i/o then put it back on the queue
					if(process_array[i].i_o_burst == 1):
						process_array[i].i_o_burst -= 1

						if(process_array[i].cpu_time > 0):
						

							#now we determine if its going to be running or ready be careful because since we have an array
							#within this for loop we could have added to the queue
							if(len(process_queue) == 0):

								#if it is the first one to be on the ready queue then we compute all the neccesary parameters
								#problem is here where if if just got blocked
								process_array[i].current_state = "running"

								#compute the cpu burst
								#calculate the randomOS time for the single burst
								process_array[i].cpu_burst = randomOS(process_array[i].b_value)
								process_array[i].original_cpu_burst = process_array[i].cpu_burst

								if(process_array[i].cpu_burst > quantum):
									process_array[i].cpu_burst = quantum								

								#if the burst is greater than the cpu time left set it equal to that
								if(process_array[i].cpu_burst > process_array[i].cpu_time):
									process_array[i].original_cpu_burst = process_array[i].cpu_time

								#calcualte the I/O burst
								process_array[i].i_o_burst = process_array[i].original_cpu_burst * process_array[i].multiplier

								process_queue.append(process_array[i])
								removal_list2.append(process_array[i])


							#otherwise we know that it isn't the first
							else:
								process_array[i].current_state = "ready"
								process_queue.append(process_array[i])
								removal_list2.append(process_array[i])

						#we know that cpu time isnt done
						else:
							process_array[i].current_state = "terminated"


					#otherwise it is not done blocking
					else:
						process_array[i].i_o_burst -= 1

			for i in range(0,len(removal_list2)):
				blocking_list.remove(removal_list2[i])

		
		if(len(unstarted_list) > 0):

			for i in range(0,len(unstarted_list)):

				make_run = True
				removal_list_unstarted = []

				for j in range(0,len(process_queue)):

					if(process_queue[j].current_state == "running"):
						make_run = False

				if(make_run):
					unstarted_list[i].current_state = "running"
					#compute the cpu burst
					#calculate the randomOS time for the single burst
					unstarted_list[i].cpu_burst = randomOS(unstarted_list[i].b_value)
					unstarted_list[i].original_cpu_burst = unstarted_list[i].cpu_burst

					if(unstarted_list[i].cpu_burst > quantum):
						unstarted_list[i].cpu_burst = quantum					

					#if the burst is greater than the cpu time left set it equal to that
					if(unstarted_list[i].cpu_burst > unstarted_list[i].cpu_time):
						unstarted_list[i].original_cpu_burst = unstarted_list[i].cpu_time

					#calcualte the I/O burst
					unstarted_list[i].i_o_burst = unstarted_list[i].original_cpu_burst * unstarted_list[i].multiplier

					process_queue.append(unstarted_list[i])
					removal_list_unstarted.append(unstarted_list[i])


				else:
					unstarted_list[i].current_state = "ready"
					process_queue.append(unstarted_list[i])
					removal_list_unstarted.append(unstarted_list[i])

			for i in range(0,len(removal_list_unstarted)):
				unstarted_list.remove(removal_list_unstarted[i])

		if(len(temp_array) > 0):
			for i in range(0,len(temp_array)):
				if(temp_array[i].current_state == "blocked"):
					temp_array[i].time_waited += 1
					blocking_list.append(temp_array[i])
					temp_array.remove(temp_array[i])
			
		#check if the processes are terminated
		for i in range(0,len(process_array)):
			if(process_array[i].current_state == "terminated"):
				check_sum += 1

		
		#check to see if everything is terminated
		if(check_sum == num_process):
			all_terminated = True

		#update the waiting time, i/o time etc here after each cycle
		for i in range(0,len(process_array)):

			if(process_array[i].current_state == "blocked" and process_array[i].i_o_burst != 0):
				process_array[i].input_output_time += 1

			elif(process_array[i].current_state == "ready"):
				process_array[i].waiting_time += 1

		
		cycle += 1
		#pdb.set_trace()
	print("The scheduling algorithm used was Round Robbin")
	print("")
	for i in range(0,len(process_array)):
		process_array[i].summary()
	full_summary(process_array,num_process)

round_robbin(process_array,2)

def shortest_job_first(new_process_array):

	all_terminated = False

	total_terminated = 0

	total_count = 0

	print_array = list(new_process_array)

	process_array = []

	#index = 0 means running, index > 0 means ready, not within the queue means blocked
	process_queue = []

	blocking_list = []

	unstarted_list = []

	cycle = 0


	while(all_terminated == False):

		#pdb.set_trace()

		if(len(new_process_array) == 0):
			pass

		elif(cycle == 0):
			if(len(new_process_array) >= 2):
				process_array.append(new_process_array.pop(0))
				process_array.append(new_process_array.pop(0))

			else:
				new_process_array[0].current_state = "running"
				#compute the cpu burst
				#calculate the randomOS time for the single burst
				new_process_array[0].cpu_burst = randomOS(new_process_array[0].b_value)

				#if the burst is greater than the cpu time left set it equal to that
				if(new_process_array[0].cpu_burst > new_process_array[0].cpu_time):
					new_process_array[0].cpu_burst = new_process_array[0].cpu_time

				#calcualte the I/O burst
				new_process_array[0].i_o_burst = new_process_array[0].cpu_burst * new_process_array[0].multiplier
				process_queue.append(new_process_array.pop(0))

		else:

			#check if a process was terminated if it was then we add a process
			if(total_terminated > total_count):
				total_count = total_terminated
				process_queue.append(new_process_array.pop(0))

			else:
				for i in range(0,len(new_process_array)):

					if(new_process_array[i].current_state == "unstarted" and (new_process_array[i].arrival_time == cycle)):
						new_process_array[i].current_state = "ready"
						new_process_array[i].waiting_time += 1

					elif(new_process_array[i].current_state == "ready" and (new_process_array[i].arrival_time < cycle)):
						new_process_array[i].waiting_time += 1		

		check_sum = 0

		if(VERBOSE_FLAG):
			verbose_function(print_array,cycle)

		#pdb.set_trace()
		
		#this is the initial check getting processes from state: unstarted to ready or running
		for i in range(0,len(process_array)):


			if((process_array[i].current_state == "unstarted") and (process_array[i].arrival_time == 0)):

				#we want to add it only if we wont be adding something before from previous runs
				process_queue.append(process_array[i])	

			elif((process_array[i].current_state == "unstarted") and (process_array[i].arrival_time == cycle) and (cycle > 0)):

				#wait until the end to add it so we can make changes
				unstarted_list.append(process_array[i])

			#will need to check to put back into process_queue when its unblocked

		#now go through the loop and update processes based on their positions #using the "queue" array

		if(len(process_queue) > 0):

			make_pop = False
			pop_array = []


			for i in range(0,len(process_queue)):


				#check if has been set to running yet if it is unstarted or a first arrived ready process
				if(((process_queue[i].current_state == "unstarted") or (process_queue[i].current_state == "ready") or (process_queue[i].current_state == "blocked")) and (i == 0)):

					process_queue[i].current_state = "running"


					#compute the cpu burst
					#calculate the randomOS time for the single burst
					process_queue[i].cpu_burst = randomOS(process_queue[i].b_value)

					#if the burst is greater than the cpu time left set it equal to that
					if(process_queue[i].cpu_burst > process_queue[i].cpu_time):
						process_queue[i].cpu_burst = process_queue[i].cpu_time

					#calcualte the I/O burst
					process_queue[i].i_o_burst = process_queue[i].cpu_burst * process_queue[i].multiplier

				


				elif((process_queue[i].current_state == "blocked") and (i >0)):

					if(process_queue[i].i_o_burst == 1):
						process_queue[i].i_o_burst -= 1

					if(process_queue[0].current_state == "terminated" or process_queue[0].current_state == "blocked" and i==1):
						process_queue[i].current_state = "running"

					else:
						process_queue[i].current_state = "ready"


				#if the first index process is running then we compute how much more is it running for
				elif((process_queue[i].current_state == "running") and (i == 0)):

					if(process_queue[i].cpu_burst > 0):
						process_queue[i].cpu_burst -= 1

					if(process_queue[i].cpu_time > 0):
						process_queue[i].cpu_time -= 1



					#now figure out whether to turn into blocked process or terminated else keep running and same position
					if((process_queue[i].cpu_burst == 0) and (process_queue[i].cpu_time == 0)):
						
						process_queue[i].current_state = "terminated"
						process_queue[i].finishing_time = cycle
						process_queue[i].turn_around_time = process_queue[i].finishing_time - process_queue[i].arrival_time
						#now pop the process because we are done with running it
						total_terminated += 1
						pop_array.append(process_queue[i])

					#now we are blocking the process
					elif((process_queue[i].cpu_burst == 0) and (process_queue[i].cpu_time > 0)):
						process_queue[i].current_state = "blocked"
						pop_array.append(process_queue[i])


					#we keep it running
					#else:


				#we are not checking for terminated because it should not be in here
				elif((i > 0) and ((process_queue[i].current_state =="blocked") or (process_queue[i].current_state =="unstarted")) and ((process_queue[0].current_state !="blocked"))):
					
					#print(process_queue[i].toString(),process_queue[i].current_state)
					process_queue[i].current_state = "ready"


				#if we havent popped the done process in first index we change the next process behind it to running
				#assuming that the previous run we have index 0 running and index 1 had been changed to ready
				elif((len(process_queue) > 1) and ((process_queue[0].current_state =="blocked") or (process_queue[0].current_state =="terminated"))):

					if(process_queue[0].index != process_queue[1].index):
						process_queue[1].current_state = "running"

						
						#compute the cpu burst
						#calculate the randomOS time for the single burst
						process_queue[1].cpu_burst = randomOS(process_queue[1].b_value)

						#if the burst is greater than the cpu time left set it equal to that
						if(process_queue[1].cpu_burst > process_queue[1].cpu_time):
							process_queue[1].cpu_burst = process_queue[1].cpu_time


						#calcualte the I/O burst
						process_queue[1].i_o_burst = process_queue[1].cpu_burst * process_queue[1].multiplier


			temp_array = []

			if(len(pop_array) > 0):
				# save this for later blocking_list.append(process_queue.pop(0))
				for i in range(0,len(pop_array)):

					if(pop_array[i].current_state == "terminated"):
						process_queue.remove(pop_array[i])
					else:
						temp_array.append(pop_array[i])
						process_queue.remove(pop_array[i])
				pop_array = []

			
			#if it is turned to blocking above it will then set this
			#update any blocked processes
			if(len(blocking_list) > 0):

				removal_list = []

				for i in range(0,len(blocking_list)):


					#if it is done with i/o then put it back on the queue
					if(blocking_list[i].i_o_burst == 1):
						

						

						#now we determine if its going to be running or ready
						if(len(process_queue) == 0):

							#pdb.set_trace()

							if(blocking_list[i].time_waited > 0):

								#problem here is if it just got blocked
								blocking_list[i].current_state = "running"
								blocking_list[i].time_waited = 0
								

								#compute the cpu burst
								#calculate the randomOS time for the single burst
								blocking_list[i].cpu_burst = randomOS(blocking_list[i].b_value)

								#if the burst is greater than the cpu time left set it equal to that
								if(blocking_list[i].cpu_burst > blocking_list[i].cpu_time):
									blocking_list[i].cpu_burst = blocking_list[i].cpu_time

								#calcualte the I/O burst
								blocking_list[i].i_o_burst = blocking_list[i].cpu_burst * blocking_list[i].multiplier

								process_queue.append(blocking_list[i])
								removal_list.append(blocking_list[i])

							else:
								blocking_list[i].time_waited += 1



								

						#otherwise we know that it isn't the first
						else:

							if(blocking_list[i].time_waited > 0):

								#check if the current process that is first on the index is blocked or terminated and just hasnt been popped yet
								if((process_queue[0].current_state == "terminated") or (process_queue[0].current_state == "blocked") and (i>0)):
									
									blocking_list[i].current_state = "running"
									blocking_list[i].time_waited = 0
									
									#compute the cpu burst
									#calculate the randomOS time for the single burst
									blocking_list[i].cpu_burst = randomOS(blocking_list[i].b_value)

									#if the burst is greater than the cpu time left set it equal to that
									if(blocking_list[i].cpu_burst > blocking_list[i].cpu_time):
										blocking_list[i].cpu_burst = blocking_list[i].cpu_time


									#calcualte the I/O burst
									blocking_list[i].i_o_burst = blocking_list[i].cpu_burst * blocking_list[i].multiplier
									process_queue.append(blocking_list[i])
									removal_list.append(blocking_list[i])
									


								elif((process_queue[0].current_state == "running")):

									##try making it so that if you know that it is a smaller index and only has 1 cpu burst left
									blocking_list[i].current_state = "ready"
									blocking_list[i].time_waited = 0

									process_queue.append(blocking_list[i])
									removal_list.append(blocking_list[i])
							else:
								blocking_list[i].time_waited += 1
								
					

					#otherwise it is not done blocking
					else:
						blocking_list[i].i_o_burst -= 1
						blocking_list[i].time_waited += 1

				for i in range(0,len(removal_list)):
					blocking_list.remove(removal_list[i])	
			
		#this is if there are no more process ready or running
		elif(len(process_queue)==0):

			removal_list2 = []

			for i in range(0,len(print_array)):

				if(print_array[i].current_state == "blocked"):

					#calculate the i_o time left

					#if it is done with i/o then put it back on the queue
					if(print_array[i].i_o_burst == 1):
						print_array[i].i_o_burst -= 1

						if(print_array[i].cpu_time > 0):
						

							#now we determine if its going to be running or ready be careful because since we have an array
							#within this for loop we could have added to the queue
							if(len(process_queue) == 0):

								#if it is the first one to be on the ready queue then we compute all the neccesary parameters
								#problem is here where if if just got blocked
								print_array[i].current_state = "running"
								


								#compute the cpu burst
								#calculate the randomOS time for the single burst
								print_array[i].cpu_burst = randomOS(print_array[i].b_value)

								#if the burst is greater than the cpu time left set it equal to that
								if(print_array[i].cpu_burst > print_array[i].cpu_time):
									print_array[i].cpu_burst = print_array[i].cpu_time

								#calcualte the I/O burst
								print_array[i].i_o_burst = print_array[i].cpu_burst * print_array[i].multiplier

								process_queue.append(print_array[i])
								removal_list2.append(print_array[i])


							#otherwise we know that it isn't the first
							else:
								print_array[i].current_state = "ready"
								process_queue.append(print_array[i])
								removal_list2.append(print_array[i])

						#we know that cpu time isnt done
						else:
							print_array[i].current_state = "terminated"
							total_terminated += 1


					#otherwise it is not done blocking
					else:
						print_array[i].i_o_burst -= 1

			for i in range(0,len(removal_list2)):
				blocking_list.remove(removal_list2[i])

		
		if(len(unstarted_list) > 0):

			for i in range(0,len(unstarted_list)):

				make_run = True
				removal_list_unstarted = []

				for j in range(0,len(process_queue)):

					if(process_queue[j].current_state == "running"):
						make_run = False

				if(make_run):
					unstarted_list[i].current_state = "running"
					#compute the cpu burst
					#calculate the randomOS time for the single burst
					unstarted_list[i].cpu_burst = randomOS(unstarted_list[i].b_value)

					#if the burst is greater than the cpu time left set it equal to that
					if(unstarted_list[i].cpu_burst > unstarted_list[i].cpu_time):
						unstarted_list[i].cpu_burst = unstarted_list[i].cpu_time

					#calcualte the I/O burst
					unstarted_list[i].i_o_burst = unstarted_list[i].cpu_burst * unstarted_list[i].multiplier

					process_queue.append(unstarted_list[i])
					removal_list_unstarted.append(unstarted_list[i])


				else:
					unstarted_list[i].current_state = "ready"
					process_queue.append(unstarted_list[i])
					removal_list_unstarted.append(unstarted_list[i])

			for i in range(0,len(removal_list_unstarted)):
				unstarted_list.remove(removal_list_unstarted[i])

		if(len(temp_array) > 0):
			for i in range(0,len(temp_array)):
				if(temp_array[i].current_state == "blocked"):
					temp_array[i].time_waited += 1
					blocking_list.append(temp_array[i])
					temp_array.remove(temp_array[i])
			
		#check if the processes are terminated
		for i in range(0,len(print_array)):
			if(print_array[i].current_state == "terminated"):
				check_sum += 1
		total_terminated = check_sum

		
		#check to see if everything is terminated
		if(check_sum == num_process):
			all_terminated = True

		#update the waiting time, i/o time etc here after each cycle
		for i in range(0,len(process_array)):

			if(process_array[i].current_state == "blocked" and process_array[i].i_o_burst != 0):
				process_array[i].input_output_time += 1

			elif(process_array[i].current_state == "ready"):
				process_array[i].waiting_time += 1

		
		cycle += 1
		#pdb.set_trace()
	print("The scheduling algorithm used was Shortest Job First")
	print("")
	for i in range(0,len(print_array)):
		print_array[i].summary()
	full_summary(print_array,num_process)

#shortest_job_first(process_array)






