#!/usr/bin/env python
import sys
import pdb


#this is the class that will maintain the properties for each task
class Task:

	def __init__(self,task_num,resource_num):
		self.task_num = task_num
		self.time_take = 0
		self.waiting_time = 0
		self.activity_number = 0
		self.terminated = False
		self.resource_in_use = dict()
		self.state = dict()
		self.final_state = 'unfinished'
		self.current_wait_time = 0

		#this is because if we have multiple resources we will need to have different states for them
		for i in range(1,resource_num+1):
			self.state[i] = 'unstarted' 

		#we will use a list of commands that each task
		#will hope to perform during each cycle 
		self.list_of_tasks = dict()

		#this will be used to know on what line of the activities within a specific task we are executing
		self.activity_index = 0

		#use this in order to help figure out when there are deadlocks
		self.wait_list = dict()




	def toString(self):
		return 'Task '+str(self.task_num)


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
		task = Task(i,num_resources)
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
		task.current_wait_time = 0
		task.state[resource_type]  = 'running'
		


	else:
		task.waiting_time += 1
		task.current_wait_time += 1
		task.state[resource_type] = 'waiting'
		



#this method returns the resources back to the "general pool" by subtracting what the 
#current task has as input, we also use temp_resources because we have to wait a whole cycle
#before another task can use the resources so this acts as an artifical time delay
def release_resource(resource_type,temp_resources,task):

	if(resource_type in task.resource_in_use):
		resources_used = task.resource_in_use[resource_type]
		del task.resource_in_use[resource_type]

		if(resource_type in temp_resources):
			temp_resources[resource_type] += resources_used
		else:
			temp_resources[resource_type] = resources_used	

		#update the task indexing element and get rid of the top activity line
		# del task.list_of_tasks[task.activity_index]
	task.activity_index += 1
	task.current_wait_time = 0


#this method will reconcile the temp_resource dict and resource dict, and we 
#are creating this method in order to modularize the code
def reconcile_resources(resources,temp_resources):

	for temp in temp_resources:
		resources[temp] += temp_resources[temp]

#this method checks to see if there is a deadlock of the resource
#and if there is then it will abort the lowest numbered deadlocked task and return true otherwise false
def check_deadlock(resource_type,resources,task_array,num_task,temp_resources):


	resource_left = resources[resource_type]

	temp_resources_left = 100

	#just in case in the second round there will be resources available
	if(resource_type in temp_resources):
		temp_resources_left = temp_resources[resource_type]


	#this will keep record of how many tasks may potentially be in deadlock
	count_dead_lock = 0
	count_terminated = 0
	abort_list = []	



	for i in range(0,len(task_array)):

		#here we are checking to see what is the current activity that the task is going to perform
		#if this ends up being the same as the resource and it has previously waited 
		#for the resource then we know there is a deadlock 
		activity_line = task_array[i].list_of_tasks[task_array[i].activity_index]
		if(((task_array[i].state[resource_type] != 'terminated') and (task_array[i].state[resource_type] != 'aborted')) and (activity_line[0] == 'request') and (activity_line[2] > resource_left or activity_line[2] > temp_resources_left)):

			if(task_array[i].state[resource_type] == 'waiting'):
				count_dead_lock += 1
				abort_list.append(task_array[i])

		elif(task_array[i].state[resource_type] == 'terminated' or (task_array[i].final_state == 'aborted')):
			count_terminated += 1


	if(count_dead_lock == (num_task-count_terminated) and (count_dead_lock != 0)):

		#check to make sure that the task has resources regardless whether it will be aborted
		if(resource_type in abort_list[0].resource_in_use):
			release_resource(resource_type,resources,abort_list[0])

		#otherwise
		abort_list[0].terminated = True
		abort_list[0].state[resource_type] = 'aborted'
		abort_list[0].final_state = 'aborted'

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

		if(task_array[i].final_state == 'aborted'):
			output_string += 'Task ' + str(task_array[i].task_num) + '\t\t' + 'aborted\n'

		else:
			sum_finish += task_array[i].time_take
			total_wait += task_array[i].waiting_time			
			output_string += 'Task ' + str(task_array[i].task_num) + '\t\t' + str(task_array[i].time_take) + '\t' + str(task_array[i].waiting_time) + '\t' + str(task_array[i].waiting_time/task_array[i].time_take)+'%\n'


	output_string += 'total  \t\t' + str(sum_finish) + '\t' + str(total_wait) + '\t' +  str(total_wait/sum_finish)+'%'

	print(output_string)


def allocation_process(resource_type,task_array,resources,temp_resources,cycle):

	#pdb.set_trace()


	#check if we have to initiate any of the tasks
	for i in range(0,len(task_array)):

		compute_flag = False

		current_task = task_array[i].list_of_tasks[task_array[i].activity_index]

		current_activity = current_task[0]
		current_resource = current_task[1]
		num_requested = current_task[2]	
		print(task_array[i].toString(),current_activity,current_resource,num_requested)	
		
		#pdb.set_trace()

		for j in task_array[i].list_of_tasks:
			if(task_array[i].list_of_tasks[j][0] == 'compute'):
				compute_flag = True

		if(current_activity == 'compute' and task_array[i].final_state == 'computing'):
			#in this case num_requested is the wait time
			print(task_array[i].list_of_tasks[task_array[i].activity_index][1])
			if(num_requested > 0):
				task_array[i].waiting_time += 1
				task_array[i].list_of_tasks[task_array[i].activity_index][2] = task_array[i].list_of_tasks[task_array[i].activity_index][2] - 1


			else:
				task_array[i].final_state = 'running'
				task_array[i].activity_index += 1	

		#this is when we see it for the first time
		elif(current_activity == 'compute' and task_array[i].final_state != 'computing'):
			task_array[i].final_state = 'computing'

		elif(current_resource != resource_type and (current_resource != 0)):
			continue		

		#this is going to have to be like state+i 
		elif(task_array[i].state[resource_type] == 'unstarted'):

			current_task = task_array[i].list_of_tasks[task_array[i].activity_index]

			# current_resource = current_task[1]
			# num_requested = current_task[2]

		#this is if we were aborting immediately after seeing what was initially requested
		# if(num_requested > resources[current_resource]):
		# 	task_array[i].state = 'aborted'

		# else:
			task_array[i].state[resource_type] = 'started'			

			#then incrementing the index for the next line
			task_array[i].activity_index += 1


		#deal with a task that was aborted here
		elif(task_array[i].state[resource_type] == 'aborted'):
			# #this is just so we don't continuously update the time the task finished
			# if(task_array[i].time_take == 0):
			# 	task_array[i].time_take = cycle 			
			pass


		#otherwise we begin to do the other requests/releases etc.
		else:


			#now determine which function to use based upon the activity retrieved
			if(current_activity == 'request'):

				request_resource(num_requested,current_resource,resources,task_array[i])

			elif(current_activity == 'release'):

				release_resource(current_resource,temp_resources,task_array[i])


				if(task_array[i].list_of_tasks[task_array[i].activity_index][0] == 'terminate' and compute_flag == True):
					task_array[i].final_state = 'terminated'


			else:

				task_array[i].state[resource_type] = 'terminated'

				# #this is just so we don't continuously update the time the task finished
				# if(task_array[i].time_take == 0):
				# 	task_array[i].time_take = cycle 
	print()

def prioritize_dict(resource_type,task_array):

	ret_array = []

	for i in range(0,len(task_array)):

		if(task_array[i].state[resource_type] == 'waiting'):

			if(len(ret_array) == 0):
				ret_array.append(task_array[i])
			else:


				for j in range(0,len(ret_array)):

					if(task_array[i].current_wait_time > ret_array[j].current_wait_time):
						ret_array.insert(j,task_array[i])
						break
						
					if(j == len(ret_array)-1):
						ret_array.append(task_array[i])


	#add the remaining
	for i in range(0,len(task_array)):
		if(task_array[i].state[resource_type] != 'waiting'):
			ret_array.append(task_array[i])

	return ret_array

def fifo_manager(task_array,num_task,resources,num_resources):

	cycle = 0

	finished = False


	while(finished != True):

		#use this to delay the releasing of resources
		temp_resources = dict()

		for i in resources:

			temp_array = prioritize_dict(i,task_array)

			allocation_process(i,temp_array,resources,temp_resources,cycle)
	
			#now check to see if there is a deadlock at the end of the cycle by looking
			#through every resource
			for i in resources:

				#we keep it in a while loop in order to see if we have to abort multiple tasks
				while(check_deadlock(i,resources,task_array,num_task,temp_resources)):
					pass
				
			
		#### validation part ####	

		#check to see if a task has fully been terminated aka done with all of its resources
		for i in range(0,len(task_array)):
			#number of resources termianted needs to equal number of resources
			num_terminated = 0
			for j in resources:
			
				if(task_array[i].final_state != 'aborted' and task_array[i].state[j] == 'terminated'):
					num_terminated += 1

			if(num_terminated == num_resources):
				task_array[i].final_state = 'terminated'
				

		total_finish = 0
		
		#now check to see if every task has finished
		for i in range(0,len(task_array)):
			if(task_array[i].final_state == 'terminated' or task_array[i].final_state == 'aborted'):
				#this is in order to make sure that we are not repeatedly changing the finish time
				if(task_array[i].time_take == 0):
					task_array[i].time_take = cycle

				total_finish += 1


		if(total_finish == num_task):
			finished = True

		print(resources,temp_resources)
		
		reconcile_resources(resources,temp_resources)

		#we add by num_resources because within the while loop we are performing the actions
		#of multiple resources in parallel
		cycle += num_resources



task_array,num_task,resources,num_resources  = start_up()

fifo_manager(task_array,num_task,resources,num_resources)

print_output('FIFO',task_array)




