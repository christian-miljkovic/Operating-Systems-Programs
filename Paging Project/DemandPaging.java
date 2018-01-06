import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.*;

/*

author Christian Miljkovic
*/

public class DemandPaging {

	private static final double totalEvictions = 0;

	public static void main(String[] args) {
		
		//storing command line arguments 
		int M = Integer.parseInt(args[0]);
		int P = Integer.parseInt(args[1]);
		int S = Integer.parseInt(args[2]);
		int J = Integer.parseInt(args[3]);
		int N = Integer.parseInt(args[4]);
		String algorithm = args[5];
		
		//this is to match the output
		System.out.println("The machine size is "+M);
		System.out.println("The page size is "+P);
		System.out.println("The process size is "+S);
		System.out.println("The job mix number is "+J);
		System.out.println("The number of references per process is "+N);
		System.out.println("The replacement algorithm is "+algorithm+"\n\n");
		
		
		//attempt to read in the RandomInts.txt file
		Scanner intScanner = null; 
		try {
			intScanner = new Scanner(new File("random-ints.txt"));
			
			
		} catch (Exception e) {
			System.err.printf("Error: there was a problem reading the random file");
			System.exit(0);
		}
		
		int quantum = 3;
		
		Process currentProcess;
		ArrayList<Process> processList = new ArrayList<Process>();
		
		//check now to see the job mix
		if(J == 1){	
			//int processNumber, double a, double b, double c, int size, int numberOfReferences, int numberOfPages,Scanner randInt, String replacementAlgo
			currentProcess = new Process(1,1,0,0,S,N,S/P,intScanner,algorithm);
			processList.add(currentProcess);
		}
		else if(J ==2) {
			
			for (int i = 0; i < 4; i++) {
				currentProcess = new Process(i+1,1,0,0,S,N,S/P,intScanner,algorithm);
				processList.add(currentProcess);
			}
		}
			
		else if (J == 3){
			for (int i = 0; i < 4; i++) {
				currentProcess = new Process(i+1,0,0,0,S,N,S/P,intScanner,algorithm);
				processList.add(currentProcess);
			}
		}
			
		else {
			//1,2,3,4
			currentProcess = new Process(1,0.75,0.25,0,S,N,S/P,intScanner,algorithm);
			processList.add(currentProcess);
			currentProcess = new Process(2,0.75,0,0.25,S,N,S/P,intScanner,algorithm);
			processList.add(currentProcess);
			currentProcess = new Process(3,0.75,0.125,0.125,S,N,S/P,intScanner,algorithm);
			processList.add(currentProcess);
			currentProcess = new Process(4,0.5,0.125,0.125,S,N,S/P,intScanner,algorithm);
			processList.add(currentProcess);
			
		}
		
		//get the size of the frame table depending upon machine size and page size
		//remember we are also going to use the highest most frame as the first one
		int sizeOfFrame = M/P -1;
		
		
		//these are going to simply help us determine which frame is to be evicted if neccesary
        //linked list for LRU replacement algorithm
        LinkedList<Integer> LRUList = new LinkedList<Integer>();

        // we do not need a data structure for LIFO either because we will always replace the last frame
        
        //we do not need to use one for random since we do not need to keep track of which page we are getting rid of
        
		//this is going to hold the current process,page pair in each index so it will look like <1,{Process,page}>
        //having the Integer array will help us replace and update the frame easier then just maintaining if there's something in the map
		HashMap<Integer, Integer[]> frame = new HashMap<Integer, Integer[]>(); 
		
		int time = 1;
		
		for(int i=0; i < processList.size() * N; i++) {
			//get the current process
			Process runningProcess = processList.get(i%processList.size());
			
			if(runningProcess.numberOfReferences <= 0) {
				//then the process is done running
				time++;
				break;
				
			}
			// this is simply to simulate the round robin simulation
			for(int j=0; j < quantum; j++) {
				
				if(runningProcess.numberOfReferences <= 0) {
					//then the process is done running					
					break;
					
				}
				
				int currentRef = runningProcess.currentReference;
				
				//now get the page index then check if it is MAX_VALUE or within the frame
				int pageIndex = currentRef/P;
				int processFrameIndex = runningProcess.pages[pageIndex];
				

				//we know we had a miss because the page table is not in the frame
				if(processFrameIndex == Integer.MAX_VALUE) {
					
					runningProcess.pageFaults++;
					
					
					//now we determine where to place the pageTable in the frame
					//we know that if it is less than zero then there is no room on the frame table since we start from highest index
					if(sizeOfFrame < 0) {
						//then we must use some sort of replacement algorithm
						if(runningProcess.replacementAlgo.equalsIgnoreCase("LIFO")) {
							
							//pop the last frame and get the necessary information
							Integer[] removeProcessPagePair = frame.remove(0);
							int removeIndex = removeProcessPagePair[0];
							int nullifyPageIndex = removeProcessPagePair[1];
							
							//get the actual process from the process list and update its values
							Process updateProcess = processList.get(removeIndex);
							updateProcess.pages[nullifyPageIndex] = Integer.MAX_VALUE;
							updateProcess.numberOfEvictions++;
							updateProcess.residencyTime += time - updateProcess.pageLoadTime[nullifyPageIndex];
							updateProcess.pageLoadTime[nullifyPageIndex] = 0;
							
							sizeOfFrame++;
							
							//update the pages array
							runningProcess.pages[pageIndex] = sizeOfFrame;
							runningProcess.pageLoadTime[pageIndex] = time;
							
							//we will need to know which process to update and remember that to get processNum 1 
							//in the array list that is at index 0. Then to update its pageTable we will also need its pageIndex
							Integer[] processPagePair = {runningProcess.processNumber-1,pageIndex};
							frame.put(sizeOfFrame, processPagePair);
							
							sizeOfFrame--;
							
						}
						else if(runningProcess.replacementAlgo.equalsIgnoreCase("LRU")) {
														
							//remove the top of the LRULinked List and get the index of the frame
							int indexRemoveFrame = LRUList.remove();

							
							
							
							//pop the index of the frame and get the necessary information
							Integer[] removeProcessPagePair = frame.remove(indexRemoveFrame);
							int removeIndex = removeProcessPagePair[0];
							int nullifyPageIndex = removeProcessPagePair[1];
							
							//get the actual process from the process list and update its values
							Process updateProcess = processList.get(removeIndex);
							updateProcess.pages[nullifyPageIndex] = Integer.MAX_VALUE;
							updateProcess.numberOfEvictions++;
							updateProcess.residencyTime += time - updateProcess.pageLoadTime[nullifyPageIndex];
							updateProcess.pageLoadTime[nullifyPageIndex] = 0;
							
							//now add to the back of the linked list the most newly updated indexFrame
							LRUList.add(indexRemoveFrame);
							
							//update the running process
							runningProcess.pages[pageIndex] = indexRemoveFrame;
							runningProcess.pageLoadTime[pageIndex] = time;
							
							//we will need to know which process to update and remember that to get processNum 1 
							//in the array list that is at index 0. Then to update its pageTable we will also need its pageIndex
							Integer[] processPagePair = {runningProcess.processNumber-1,pageIndex};
							frame.put(indexRemoveFrame, processPagePair);
							
						}
						
						//this indicates it is random replacement algorithm
						else if(runningProcess.replacementAlgo.equalsIgnoreCase("RANDOM")) {
							
							//get the random int and then find out which random frame you are taking out
							int randomInt = intScanner.nextInt();
							//since it is probably some big number we have to accommodate it for our frame size
							int randomIntIndex = (randomInt + M/P)%(M/P);
							
							//and pretty much do the same as the above but with the randomIntIndex
							//pop the index of the frame and get the necessary information
							Integer[] removeProcessPagePair = frame.remove(randomIntIndex);
							int removeIndex = removeProcessPagePair[0];
							int nullifyPageIndex = removeProcessPagePair[1];
							
							//get the actual process from the process list and update its values
							Process updateProcess = processList.get(removeIndex);
							updateProcess.pages[nullifyPageIndex] = Integer.MAX_VALUE;
							updateProcess.numberOfEvictions++;
							updateProcess.residencyTime += time - updateProcess.pageLoadTime[nullifyPageIndex];
							updateProcess.pageLoadTime[nullifyPageIndex] = 0;
							
							/////DO IF CYCLE IS IN 38 DEBUGG IN HERE/////
							
							
							//update the running process
							runningProcess.pages[pageIndex] = randomIntIndex;
							runningProcess.pageLoadTime[pageIndex] = time;
							
							//we will need to know which process to update and remember that to get processNum 1 
							//in the array list that is at index 0. Then to update its pageTable we will also need its pageIndex
							Integer[] processPagePair = {runningProcess.processNumber-1,pageIndex};
							frame.put(randomIntIndex, processPagePair);
							
							
						}
						
					}
					//otherwise we will now place the pageTable into the frame
					else {
						
						//update the pages array
						runningProcess.pages[pageIndex] = sizeOfFrame;
						runningProcess.pageLoadTime[pageIndex] = time;
						
						
						
						//we will need to know which process to update and remember that to get processNum 1 
						//in the array list that is at index 0. Then to update its pageTable we will also need its pageIndex
						Integer[] processPagePair = {runningProcess.processNumber-1,pageIndex};
						frame.put(sizeOfFrame, processPagePair);
						
						//update the LRU if the process is using the algorithm
						if(runningProcess.replacementAlgo.equalsIgnoreCase("LRU")) {
							
							//sizeOfFrame is also essentially the index of the frame
							LRUList.add(sizeOfFrame);
						}
						
						//now there is one less frame available
						sizeOfFrame--;

					}
					
					
					
				}
				//there was a page hit
				else {

					//update the most recently used page for LRU
					if(runningProcess.replacementAlgo.equalsIgnoreCase("LRU")) {
						
						 //to get it back to 0 in case we are on the last frame
						
						int removeIndex = LRUList.indexOf(processFrameIndex);

						//put to the end of the list
						
					
						int updatePage = LRUList.remove(removeIndex);
						LRUList.add(updatePage);
						 //to indicate we have no more frames incase the next reference needs a new one
					
					
						
					}
					
					
				}
				//remember this also decrements the amount of references that the process has left 
				runningProcess.getNextReference();
				time++;
				
			}
			
			
			
		}
		int totalFaults = 0;
		int totalEvictions = 0;
		double totalResidency = 0;
		
		for(int i=0; i<processList.size();i++) {
			
			if(processList.get(i).numberOfEvictions != 0) {
				totalFaults += processList.get(i).pageFaults;
				totalResidency += processList.get(i).residencyTime;
				totalEvictions += processList.get(i).numberOfEvictions;
				System.out.printf("Process Number: %d had %d faults and an average residency of %f",processList.get(i).processNumber,processList.get(i).pageFaults,processList.get(i).residencyTime/processList.get(i).numberOfEvictions);
			}
			else {
				totalFaults += processList.get(i).pageFaults;
				System.out.printf("Process Number: %d had %d faults and with no evictions an average residency of undefined",processList.get(i).processNumber,processList.get(i).pageFaults);
			}
			System.out.println("");
		}
		System.out.println("\n");
		
		
		if(totalEvictions != 0) {
			double avgTotalResidency = totalResidency/totalEvictions;
			System.out.printf("The total number of faults is %d and the overall average residency is %f", totalFaults,avgTotalResidency);
		}
		else {
			System.out.printf("The total number of faults is %d and the overall average residency is undefined", totalFaults);
		}
		System.out.println("");
		

	}
	}