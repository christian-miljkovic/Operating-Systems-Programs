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

	#simulate the processes using a while loop until each state is changed to terminate
	
	all_done = False
	cycle = 0
	terminated_array = []

	while(all_done == False):

		#create the queue like structure but with a list that we will use to facilitate first in first out
		process_list = []

		#an array to keep track of the order of ready processes
		ready_array = []

		

		#place the processes in the queue
		for i in range(0,len(process_array)):
			process_list.append(process_array[i])	

		if(VERBOSE_FLAG):
			verbose_function(process_array,cycle)
		
		#change the status of each process now and update their values using the queue
		while(len(process_list) != 0):

			process = process_list.pop(0)
			

			#we check to see first if the process is TERMINATED or if the arrival time is not yet achieved
			if(process.arrival_time > cycle or process.current_state == "terminated"):
				#do nothing
				pass

			#this is just the beginning phase when we are going from UNSTARTED to ready
			elif((process.current_state == "unstarted") and (process.arrival_time <= cycle)):

				process.current_state = "ready"
				
				#check to make sure that it isn't already there
				if((process in ready_array) == False):
					ready_array.append(process)

				# for i in range(0,len(ready_array)):
				# 	print(ready_array[i].toString(), cycle)


				if(process.index == 0):
					#if it is the first process since it is sorted we switch it to running
					process.current_state = "running"
					ready_array.remove(process)
					
					#calculate the randomOS time for the single burst
					process.cpu_burst = randomOS(process.b_value)

					#if the burst is greater than the cpu time left set it equal to that
					if(process.cpu_burst > process.cpu_time):
						process.cpu_burst = process.cpu_time

					#calcualte the I/O burst
					process.i_o_burst = process.cpu_burst * process.multiplier
					
				

			#check if the process is RUNNING
			elif(process.current_state == "running"):

				#calculate the cpu_time - cpu_burst
				process.cpu_time = process.cpu_time - process.cpu_burst

				process.cpu_burst -= 1

				#check to make sure that the cpu burst is zero or not to set into blocking or terminate
				if(process.cpu_burst == 0):

					if(process.cpu_time == 0):
						#calculate the neccesary statistics for each process
						process.current_state = "terminated"

					else:
						process.current_state = "blocked"

			#dealing with the process that is READY
			elif(process.current_state == "ready"):

				#check if it is the last process if so then treat it differently
				if(process.index == num_process-1):

					make_running = True

					for j in range(0,len(process_array)):

						if(process_array[j].current_state == "running"):
							make_running = False

					if(make_running):

						process.current_state = "running"
						#calculate the randomOS time for the single burst
						process.cpu_burst = randomOS(process.b_value)

						#if the burst is greater than the cpu time left set it equal to that
						if(process.cpu_burst > process.cpu_time):
							process.cpu_burst = process.cpu_time

						#calcualte the I/O burst
						process.i_o_burst = process.cpu_burst * process.multiplier
						break


				#we have to decide whether to keep it in ready or see if we will change it to running
				#look through the remaining processes that need to be processed in this cycle
				for i in range(0,len(process_array)):

					#first check to make sure that nothing else is running
					if(process_array[i].current_state == "running"):
						 
						 #check whether that running process that might be done next cycle
						 #we check just bigger because the processes before on the array would have already been changed

						 if((process_array[i].index < process.index) and ((process_array[i] in process_list) == False)):
						 	#then we know that it was just changed
						 	process.current_state = "ready"
						 	ready_array.append(process)
						 	break

						 elif((process_array[i].index > process.index)):
						 	if(process_array[i].cpu_burst > 1):
						 		process.current_state = "ready"
						 		ready_array.append(process)
						 		break


						 elif(process_array[i].index > process.index and (process_array[i].cpu_burst == 1)):

						 	#then check whether there is an already waiting process on the waitlist
						 	if(process in ready_array):
							 	if(ready_array.index(process) == 0):
							 		process.current_state = "running"
							 		break
							 	else:
							 		process.current_state = "running"
							 		break
						 #otherwise it has been previously changed within the same cycle
						 else:
						 	break


					#check if there is another ready process that is not the current process
					elif(process_array[i].current_state == "ready" and process_array[i].index != process.index):



						#now check which has the earliest arrival

						if(process in ready_array):

							if(ready_array.index(process) < ready_array.index(process_array[i])):
								process.current_state = "running"
								break

						#otherwise there was a process that came earlier 
						else:
							break

					#now check if unstarted
					else:
						process.current_state = "running"

				if(process.current_state == "running"):
					#calculate the randomOS time for the single burst
					process.cpu_burst = randomOS(process.b_value)

					#if the burst is greater than the cpu time left set it equal to that
					if(process.cpu_burst > process.cpu_time):
						process.cpu_burst = process.cpu_time

					#calcualte the I/O burst
					process.i_o_burst = process.cpu_burst * process.multiplier


			#now deal with a process if it is BLOCKED
			elif(process.current_state == "blocked"):

				#add to its I/O time 
				process.input_output_time += 1

				#now subtract frmo its I/O burst and if it is zero set it to ready
				process.i_o_burst -= 1

				if(process.i_o_burst == 0):

					#check to see if the cpu_time is done
					if(process.cpu_time > 0):

						#switch this if we are not making it go straight to running
						process.current_state = "running"

						#check if there are other processes running
						for i in range(0,len(process_array)):
							#if another process is running that isn't the current process then set it to ready 
							#check to make sure that it might be done running after this cycle
							if(((process_array[i].current_state == "running") or (process_array[i].current_state == "blocked")) and (process_array[i].index < process.index)):
								if(process_array[i].cpu_burst > 1):
									process.current_state = "ready"
									ready_array.append(process)
									break

								elif(process_array[i].i_o_burst >= 1):

									for j in range(process.index+1,len(process_array)):
										if(process_array[j].current_state == ("running") and (process_array[j].cpu_burst > 1)):
											process.current_state = "ready"
											ready_array.append(process)
											break
										elif(process_array[j].current_state == ("blocked") and (process_array[j].i_o_burst > 1)):
											break


							elif((process_array[i].current_state == "running") and (process_array[i].index > process.index)):
								if(process_array[i].cpu_burst > 1):
									process.current_state = "ready"
									ready_array.append(process)
									break

							#check if there is another process that is also ready and if it has an earlier arrival time
							elif((process_array[i].current_state == "ready") and (process_array[i].index > process.index)):
								process.current_state = "ready"
								ready_array.append(process)
								break

							elif((process_array[i].current_state == "ready") and (process_array[i].index < process.index) and (process.current_state=="ready")):
								process.current_state = "ready"
								ready_array.append(process)
								break								

							#check if there is another blocked process that may finish at the same time
							elif((process_array[i].current_state == "blocked") and (process_array[i].index < process.index) and (len(process_list) > process.index)):
								process.current_state = "ready"
								ready_array.append(process)
								break


						#always have to calc this when evers setting to run
						if(process.current_state == "running"):
							#calculate the randomOS time for the single burst
							process.cpu_burst = randomOS(process.b_value)

							#if the burst is greater than the cpu time left set it equal to that
							if(process.cpu_burst > process.cpu_time):
								process.cpu_burst = process.cpu_time

							#calcualte the I/O burst
							process.i_o_burst = process.cpu_burst * process.multiplier
					else:
						process.current_state = "terminated"

			if(process.current_state == "ready"):
				process.waiting_time += 1

			
		#check at the end of each cycle whether or not every single process
		#has been terminated
		check_sum = 0
		for i in range(0,len(process_array)):
			if(process_array[i].current_state == "terminated"):
				check_sum += 1
				if((process_array[i] in terminated_array) == False):
					terminated_array.append(process_array[i])
					process_array[i].finishing_time = cycle
					process_array[i].turn_around_time = process_array[i].finishing_time - process_array[i].arrival_time
				
		if(check_sum == num_process):
			all_done = True 			
		

		#get rid of any running cycles that were just in the ready_array
		for i in range(0,len(process_array)):
			if((process_array[i].current_state == "running") and (process_array[i] in ready_array)):
				ready_array.remove(process_array[i])

		#print(process_array[0].toString() + " " + process_array[0].current_state,process_array[1].toString() + " " + process_array[1].current_state,process_array[2].toString() + " " + process_array[2].current_state,)
		cycle += 1

#MAKE A FOR LOOP THAT IS GOING TO CHECK AT THE END OF EACH ROUND IF ANYTHING BESIDES READY IS DUPLICATED TO DETECT ERRORS


	print("The scheduling algorithm used was First Come First Served")
	print("")
	for i in range(0,len(process_array)):
		process_array[i].summary()

first_in_first_out(process_array)
	




