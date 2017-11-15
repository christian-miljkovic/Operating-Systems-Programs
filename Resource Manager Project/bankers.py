#!/usr/bin/env python
import sys


#this is the class that will maintain the properties for each task
class Task:

	def __init__(self,task_num):
		self.task_num = task_num
		self.time_take = 0
		self.waiting_time = 0
		self.activity_number = 0

		#we will use a list of commands that each task
		#will hope to perform during each cycle 
		self.list_of_tasks = dict()



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

task_array,num_task,resources,num_resources  = start_up()


for i in range(0,len(task_array)):
	print(task_array[i].toString())
	print(task_array[i].list_of_tasks)
	print()







