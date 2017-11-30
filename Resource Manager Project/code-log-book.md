#Code Log Book
#Christian Miljkovic
#Project: Bankers Algorithm - Operating Systems
#Friday Novemeber 24,2017


#1 Consider the problem youre attempting to solve
-trying to create a resource manager that implements a FIFO based algo, and Banker's (which uses Dijkstra)
-I have to be able to take inputs in that are sometimes not entirely in order/or uniform and be able to create task objects
-For FIFO I have to make sure that I am looking out for deadlocks, otherwise the manager simply gives the resource out first come first served process
-Otherwise using the bankers algorithm we should be able to always avoid any sort of deadlock therefore do not need deadlock detection


#2 Desribe your method for solving it
-The way that I am going to attempt to solve this is by breaking down every step and modularizing my code so that it is easy to debugg because in the past I have seen that with complex projects it quickly becomes hard to follow where errors come from


#3 Desrcibe the process of carrying out the method
-Modularity helps a lot when it comes to debugging, however, one of the issues that I always run into is probably coming from not thinking of the problem beforehand. For example, I realized that the deadlock method I was implmenting wasn't totally correct, or even more so realizing that i had to account for mutliple resources which is now going to make me have to go back and fix things, then on top of that the most important miss I had was realizing it was FIFO which means waiting tasks had first priority. This definitely increases the time spent coding, which I should figure out a way to avoid in the future. 

#4 Record what happened, and ask how it could be improved