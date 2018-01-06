import java.util.Scanner;

/*

author Christian Miljkovic
*/


public class Process {

    public int processNumber;
    
    public float numberOfEvictions;
    public int[] pages;
    public int[] pageLoadTime;
    public float residencyTime;
    public int pageFaults = 0;
    
    //these are used for probabilities of references
    public double a;
    public double b;
    public double c;
    
    //this is S
    public int size;
    public int currentReference;
    
    //this is N
    public int numberOfReferences;
    
    //so we know which page to replace
    public String replacementAlgo;
    public Scanner randInt; //used for getting the random numbers and we want this to be a scanner
    //because we will need it to read from the random file every time we call for example getNextReference

    public Process(int processNumber, double a, double b, double c, int size, int numberOfReferences, int numberOfPages,Scanner randInt, String replacementAlgo){

        this.processNumber = processNumber;
        this.a = a;
        this.b = b;
        this.c = c;
        this.size = size;
        this.replacementAlgo = replacementAlgo;
        
        this.numberOfReferences = numberOfReferences;
        this.randInt = randInt;
        this.currentReference = (processNumber*111+ size)%size;
        
        //will tell us if a page is in the frame or not
        this.pages = new int[numberOfPages];
        this.pageLoadTime = new int[numberOfPages];
        
        //populate the pages array with MAX_INTEGER so we can later determine if it is empty or not
        //MAX_INTEGER indicates it is empty
        for(int i = 0; i< this.pages.length; i++) {
        		this.pages[i] = Integer.MAX_VALUE ;
        }

    }

    public void getNextReference(){
    	
    		int randomInteger = this.randInt.nextInt();
    		
    		//decrement how many references the process has left
    		this.numberOfReferences--;
    	
    		double y = randomInteger/(Integer.MAX_VALUE + 1d);
    		
    		if(y<this.a) {
    			this.currentReference = (this.currentReference + 1 +this.size)%this.size;
    			
    		}
    		else if (y<(this.a + this.b)) {
    			this.currentReference = (this.currentReference - 5+this.size)%this.size;
    			
    		}
    		else if(y<(this.a + this.b + this.c)) {
    			this.currentReference = (this.currentReference + 4+this.size)%this.size;
    			
    		}
    		else {
    			//otherwise get another randomInt from the scanner we have
    			int nextRandoInt = this.randInt.nextInt();
    			this.currentReference = (nextRandoInt+this.size) % this.size;
    			
    		}
    		
    	
    }

}