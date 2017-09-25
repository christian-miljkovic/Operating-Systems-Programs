package homework01_202;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class DualPassLinker {

	private static ArrayList<Module> listOfModules = new ArrayList<Module>();
	private static HashMap<String, Integer> SymbolTable = new HashMap<String, Integer>();

	
	public static void main(String[] args) {

		if (args.length != 1) {
			System.err.println("Invalid input, please try again.");
			System.exit(0);
		}

		File inputFile = new File(args[0]);

		if (!inputFile.canRead()) {
			System.err.printf("Cannot read from file.");
			System.exit(0);
		}

		Scanner scanner = null;

		try {
			scanner = new Scanner(inputFile);
		} catch (FileNotFoundException e) {
			System.err.printf("File %s not found\n", inputFile.getAbsolutePath());
			System.exit(0);

		}


		
		ArrayList<String> lines = new ArrayList<String>();
		
		
		//use a while loop to run through the data, and delimit by new lines
		while(scanner.hasNextLine()) {
			
			if(!scanner.hasNext()) {
				//this is so that we don't get an exception thrown
				break;
			}
			
			else {
			
				lines.add(scanner.next());
			}
			
		}
		
		int numModules = Integer.parseInt(lines.get(0));
		for(int i=0; i<numModules; i++) {
			
			listOfModules.add(new Module());
			
		}
		
		System.out.println(lines);
		
		int countModule = 0;
		int countLine = 1;
		int index = 1;
	
		
		//here we are going to create each individual module 
		while(countModule < listOfModules.size()) {
			
			//check to see if there is a definition list here
			if(countLine % 3 == 1) {
				
				//this is if there isn't
				if (Integer.parseInt(lines.get(index)) == 0) {
					index++;
					countLine++;
				}
				
				else if(Integer.parseInt(lines.get(index)) == 1){
			
					
					//if not now we get all of the symbols defined here
					int shift = index; //this is because they come in pairs (sym,loc)
					
					while(index < shift + Integer.parseInt(lines.get(shift)) *2) {
					
						
						Symbol sym = new Symbol(lines.get(index+1), Integer.parseInt(lines.get(index + 2)));
						
						//now add the symbol to the correct module
						listOfModules.get(countModule).setSymbols(sym);
						
						index += 2;
						
					}
					
					//increment the line counter so we can check the use list now
					countLine += 1;
					index++;
					
				}
				
				//this is if there are more than 1 defined symbol in a module
				else {
					
					int shift = index + 1;
					
					int endShift = index + Integer.parseInt(lines.get(index))*2;

					
					
					
					while(shift < endShift) {
						

						
						Symbol sym = new Symbol(lines.get(shift), Integer.parseInt(lines.get(shift + 1)));
						
						System.out.println(sym.toString());
						
						//now add the symbol to the correct module
						listOfModules.get(countModule).setSymbols(sym);
						
						shift += 2;
						
					}

					
					index = endShift + 1; //to get us onto the next line

					
					countLine++;


					
				}
					
				
			}
			
			//now we are checking the next line
			if(countLine % 3 == 2) {
				
				//this is if there isn't a use list
				if (Integer.parseInt(lines.get(index)) == 0) {
					index++;
					countLine++;
				}
				
				else if(Integer.parseInt(lines.get(index)) == 1) {
					
					int shift = index + 1;
					int endShift = shift + Integer.parseInt(lines.get(index));
					
					
					
					while(shift < endShift) {
						

						
						listOfModules.get(countModule).setUseList(lines.get(shift));
						
						shift += 1;
						
					}

					
					index = endShift + 1; //to get us onto the next line
					
					countLine++;

					
				}
				
				else {
					
					int shift = index + 1;
					
					int endShift = index + Integer.parseInt(lines.get(index))*2;

					
					
					
					while(shift < endShift) {
						

						
						listOfModules.get(countModule).setUseList(lines.get(shift));
						
						shift += 2;
						
					}

					
					index = endShift + 1; //to get us onto the next line

					
					countLine++;
					
					
				}
					
			}
			
			//now we are checking the next line where we have the actual program text
			if(countLine % 3 == 0) {
				

				//get the number of lines there are now
				int nDigits = Integer.parseInt(lines.get(index));


				//then take the first integer so that you can update the base address of the module
				//if the count of modules is less than the number we need
				if(countModule != listOfModules.size() -1 ) {
					
					//add one because the base address of the first module is 0
					listOfModules.get(countModule + 1).setBaseAddress(Integer.parseInt(lines.get(index)) +
							listOfModules.get(countModule).getBaseAddress());
				}
				

				
				
				//now we are going to capture the numbers that occupy every single word in the 
				//program text portion
				int shift = index + 1;
				int endShift = shift + nDigits;
				
				while(shift < endShift) {
					
					
					//add all of the words to the module
					listOfModules.get(countModule).setWord(lines.get(shift));
					shift += 1;
					
					
					
				}

				//increment the index now
				index += Integer.parseInt(lines.get(index)) + 1;
				countLine++;

				
				
				
			}
			
			
			countModule++;
			
		}
		
		System.out.println(listOfModules.get(0).toString());
		System.out.println(listOfModules.get(1).toString());
		System.out.println(listOfModules.get(2).toString());
		System.out.println(listOfModules.get(3).toString());	
		
		//print out the symbol table
		
		
		
	}
	
	
}

