#!/usr/bin/env python
import sys
import pdb


#this is the class that will maintain the properties for each task
class Task:

	def __init__(self,task_num):
		self.task_num = task_num
		self.time_take = 0
		self.waiting_time = 0
		self.activity_number = 0
		self.terminated = False
		self.resource_in_use = dict()
		self.state = 'unstarted'

		#we will use a list of commands that each task
		#will hope to perform during each cycle 
		self.list_of_tasks = dict()

		#this will be used to know on what line of the activities within a specific task we are executing
		self.activity_index = 0

		#use this in order to help figure out when there are deadlocks
		self.wait_list = dict()




	def toString(self):
		return 'Task '+str(self.task_num) + ',' + self.state


#this method looks through an array of tasks and finds the correct task
def task_find(task_array,task_index):

	ret_task = None

	for i in range(0,len(task_array)):

		temp_task = task_array[i]

		if(temp_task.task_num == task_index):
			ret_task = temp_task

	return ret_task


#here we will read in the files and set up the tasks before running the algorithms
#The way we will set up tasks are by using the above class to insert each and every activity
#that a task may have in order from the input. Then we will also create a dictionary indicating
#the various resources and how many units each possesess. We will return an array of created Tasks with filled in properties,
#as well as the resource dictionary, number of resources in total, and number of tasks in total for furture looping
def start_up():


	task_array = []

	task_file = open(sys.argv[1])

	#get the number of tasks for reference 
	num_task = None
	num_resources = None
	resources = dict()

	#we will use this in order to determine how many values each resource has
	first_line_array = task_file.readline().split(' ')

	for i in range(0,len(first_line_array)):

		if(i == 0):
			num_task = int(first_line_array[i])

		elif(i == 1):
			num_resources = int(first_line_array[i])

		elif((i != len(first_line_array)) and (i > 1)):
			#for the dictionary subtract by one to indicate which resource its for
			#because the way we have initial input index 2 of the starting line gives us the quantity for
			#the first resource therefore i == 2 - 1 => gives us the quantity for resource 1 and so on
			resources[i-1] = int(first_line_array[i])

		elif(i == len(array_file)):
			resources[i-1] = int(first_line_array[i][0])

	
	for i in range(1,num_task+1):
		task = Task(i)
		task_array.append(task)

	
	#here we will ad the commands to each task
	for line in task_file.readlines():


		#this is essentially breaking down each line splitting by spaces, and getting rid of the spaces
		temp_task = list(filter(None,line.split(' ')))


		#check to make sure that the length of the array is greater than 1 because sometimes there are '\n' in singular arrays
		if(len(temp_task) > 1):
			
			#now retrieve the information that we will use to populate the activity dict above
			activity = temp_task[0]
			task_index = int(temp_task[1]) #this one we need as an index simply to access the array
			resource_index = int(temp_task[2])
			number_requested = int(temp_task[3][0])	


			#find the correct task that you have to update
			task_update = task_find(task_array,task_index)

			# print(task_update.toString())
			# print(task_update.list_of_tasks)

			#name a key based on the number of activities that the task has
			task_update.list_of_tasks[task_update.activity_number] = [activity,resource_index,number_requested]
			task_update.activity_number += 1


	return task_array,num_task,resources,num_resources



#this method checks to make sure that there is enough resources 
#to give out if requested, and if there is enough it will allocate the resource
def request_resource(resource_req,resource_type,resources,task):

	resource_left = resources[resource_type]

	#checking to make sure there is enough to allow to avoid deadlocks
	if(resource_req <= resource_left):
		resources[resource_type] -= resource_req

		#make sure to add to the current amount of resources if need be
		if(resource_type in task.resource_in_use):
			task.resource_in_use[resource_type] += resource_req
		else:
			task.resource_in_use[resource_type] = resource_req

		#update the task indexing element and get rid of the top activity line
		# del task.list_of_tasks[task.activity_index]
		task.activity_index += 1

	else:
		task.waiting_time += 1
		task.state = 'waiting'



#this method returns the resources back to the "general pool" by subtracting what the 
#current task has as input, we also use temp_resources because we have to wait a whole cycle
#before another task can use the resources so this acts as an artifical time delay
def release_resource(resource_type,temp_resources,task):

	resources_used = task.resource_in_use[resource_type]
	del task.resource_in_use[resource_type]

	if(resource_type in temp_resources):
		temp_resources[resource_type] += resources_used
	else:
		temp_resources[resource_type] = resources_used	

	#update the task indexing element and get rid of the top activity line
	# del task.list_of_tasks[task.activity_index]
	task.activity_index += 1


#this method will reconcile the temp_resource dict and resource dict, and we 
#are creating this method in order to modularize the code
def reconcile_resources(resources,temp_resources):

	for temp in temp_resources:
		resources[temp] += temp_resources[temp]

#this method checks to see if there is a deadlock of the resource
#and if there is then it will abort the lowest numbered deadlocked task and return true otherwise false
def check_deadlock(resource_type,resources,task_array,num_task):

	resource_left = resources[resource_type]

	#this will keep record of how many tasks may potentially be in deadlock
	count_dead_lock = 0
	abort_list = []	



	for i in range(0,len(task_array)):

		#here we are checking to see what is the current activity that the task is going to perform
		#if this ends up being the same as the resource and it has previously waited 
		#for the resource then we know there is a deadlock 
		activity_line = task_array[i].list_of_tasks[task_array[i].activity_index]
		if((activity_line[0] == 'request') and (activity_line[2] > resource_left)):

			if(task_array[i].state == 'waiting'):
				count_dead_lock += 1
				abort_list.append(task_array[i])			

	if(count_dead_lock == num_task):
		release_resource(resource_type,resources,abort_list[0])
		abort_list[0].terminated = True
		abort_list[0].state = 'aborted'

		#there was a deadlock
		return True
		

	#otherwise return false
	else:
		return False 


#this method creates the output for the program as specified by the docs
def print_output(method,task_array):

	total_wait = 0
	sum_finish = 0

	output_string = '\t\t ' + method + '\n'

	for i in range(0,len(task_array)):

		if(task_array[i].state == 'aborted'):
			output_string += 'Task ' + str(task_array[i].task_num) + '\t\t' + 'aborted\n'

		else:
			sum_finish += task_array[i].time_take
			total_wait += task_array[i].waiting_time			
			output_string += 'Task ' + str(task_array[i].task_num) + '\t\t' + str(task_array[i].time_take) + '\t' + str(task_array[i].waiting_time) + '\t' + str(task_array[i].waiting_time/task_array[i].time_take)+'%\n'


	output_string += 'total  \t\t' + str(sum_finish) + '\t' + str(total_wait) + '\t' +  str(total_wait/sum_finish)+'%'

	print(output_string)

def fifo_manager(task_array,num_task,resources,num_resources):

	cycle = 0

	total_finish = 0

	finished = False

	while(finished != True):

		#use this to delay the releasing of resources
		temp_resources = dict()

		# pdb.set_trace()

		#check if we have to initiate any of the tasks
		for i in range(0,len(task_array)):


			#LOOK AT THE NUMBER OF RESOURCES IF THERE ARE MORE THAN ONE
			#THEN HAVE TWO COLUMNS TO REPRESENT UNSTARED SECTIONS
			#MOST LIKELY WILL HAVE TO MAKE THIS PART THAT DOES THE ACTUAL 
			#FIFO PART INTO ONE FUNCTION AND RUN IT MULTIPLE TIMES
			if(task_array[i].state == 'unstarted'):

				current_task = task_array[i].list_of_tasks[task_array[i].activity_index]

				current_resource = current_task[1]
				num_requested = current_task[2]

				if(num_requested > resources[current_resource]):
					task_array[i].state = 'aborted'

				else:
					task_array[i].state = 'started'			

					#then incrementing the index for the next line
					task_array[i].activity_index += 1


			#deal with a task that was aborted here
			elif(task_array[i].state == 'aborted'):
				#this is just so we don't continuously update the time the task finished
				if(task_array[i].time_take == 0):
					task_array[i].time_take = cycle 

					#also add to the total tally of finished tasks
					total_finish += 1				


			#otherwise we begin to do the other requests/releases etc.
			else:


				current_task = task_array[i].list_of_tasks[task_array[i].activity_index]

				current_activity = current_task[0]
				current_resource = current_task[1]
				num_requested = current_task[2]

				#now determine which function to use based upon the activity retrieved
				if(current_activity == 'request'):

					request_resource(num_requested,current_resource,resources,task_array[i])
					# task_array[i].activity_index += 1

				elif(current_activity == 'release'):

					release_resource(current_resource,temp_resources,task_array[i])
					# task_array[i].activity_index += 1

				else:

					task_array[i].state = 'terminated'

					#this is just so we don't continuously update the time the task finished
					if(task_array[i].time_take == 0):
						task_array[i].time_take = cycle 

						#also add to the total tally of finished tasks
						total_finish += 1	

						#and as a fail safe check to make sure that there aren't any resources that haven't been released
						# for i in resources:
						# 	release_resource(i,resources,task_array[i])		

		cycle += 1

		#now check to see if there is a deadlock at the end of the cycle by looking
		#through every resource
		for i in resources:

			#we keep it in a while loop in order to see if we have to abort multiple tasks
			while(check_deadlock(i,resources,task_array,num_task)):
				pass
				

		#now check to see if every task has finished
		if(total_finish == num_task):
			finished = True

		reconcile_resources(resources,temp_resources)



task_array,num_task,resources,num_resources  = start_up()

fifo_manager(task_array,num_task,resources,num_resources)

print_output('FIFO',task_array)


# Stuff to easily print out
# task_array[i].toString()
# task_array[i].resource_in_use





