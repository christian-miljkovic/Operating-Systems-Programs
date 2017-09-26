import java.io.File;
import java.io.FileNotFoundException;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Scanner;
import java.util.Set;

public class DualPassLinker {

	private static ArrayList<Module> listOfModules = new ArrayList<Module>();
	private static ArrayList<Integer> memoryMap = new ArrayList<Integer>();
	

	
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
						

						
						listOfModules.get(countModule).setUseList(lines.get(shift),
								Integer.parseInt(lines.get(shift+1)));
						
						shift += 1;
						
					}

					
					index = endShift + 1; //to get us onto the next line
					
					countLine++;

					
				}
				
				else {
					
					int shift = index + 1;
					
					int endShift = index + Integer.parseInt(lines.get(index))*2;

					
					
					
					while(shift < endShift) {
						

						
						listOfModules.get(countModule).setUseList(lines.get(shift),
								Integer.parseInt(lines.get(shift+1)));
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
		
		//print out the symbol table
		int moduleSize = listOfModules.size();
		System.out.println("Symbol Table:");
		
		for(int i=0; i< moduleSize; i++) {
			
			Module mod = listOfModules.get(i);
			
			//check if each individual module has a symbol in it
			int numSymbol = mod.getSymbols().size();
			
			if(numSymbol > 0) {
				
				for(int j=0; j< numSymbol; j++) {
					
					mod.getOneSymbol(j).setRealAddress(mod.getBaseAddress() + 
							mod.getOneSymbol(j).getAddress());
					
					System.out.println(mod.getOneSymbol(j).toString(mod.getBaseAddress()));
		
				}
				
			}
			
		}

		
		
		//now complete the second pass and do the memory map
		for(int moduleNumber=0; moduleNumber < listOfModules.size(); moduleNumber++) {
			
			ArrayList<String> currentWordList = listOfModules.get(moduleNumber).getWord();
			
			//get the use list and create a counter for the correct symbol you have to use
			//based upon the sentinel 
			int sentinelCounter = -1;
			
			//this contains reference symbols that show the location that the symbol was used
			//within the individual module
			HashMap<String, Integer> useList = listOfModules.get(moduleNumber).getUseList();
			
			//these are the actual keys/symbols that we will need to compute their address 
			//which we will later change individual words
			String[] actualUseList = useList.keySet().toArray(new String[useList.size()]);

			
			ArrayList<Integer> useListLocations = new ArrayList<Integer>();
			
			
			//fill the useListLocations with the correct locations
			for(int i = 0; i<actualUseList.length; i++) {
				
				int symbolAddress = findLocation(actualUseList[i]);
				useListLocations.add(symbolAddress);
				
			}
		
			
			for(int wordNumber=0; wordNumber < currentWordList.size(); wordNumber++) {
				
				//now check each and every individual word and change the values if necessary
				//first look at the last number
				String currentWord = currentWordList.get(wordNumber);
				
				//add the char value to an empty string before parsing the int because parseInt
				//only takes a String not char
				int lastNum = Integer.parseInt((""+ currentWord.charAt(currentWord.length() - 1)));
				
				//now check what to do with the rest of the word based on the last number
				
				//in this case don't do anything to the address except get rid of the last
				//digit
				if(lastNum == 1 || lastNum == 2) {
					
					String address = currentWord.substring(0, currentWord.length()-1);
					int intAddress = Integer.parseInt(address);
					memoryMap.add(intAddress);
				}
				
				//add the base address to the current address
				else if(lastNum == 3) {
					
					String address = currentWord.substring(0, currentWord.length()-1);
					int intAddress = Integer.parseInt(address);
					int baseAddress = listOfModules.get(moduleNumber).getBaseAddress();
					
					int newAddress = intAddress+baseAddress;
					memoryMap.add(newAddress);
					
				}
				
				//have to resolve the external 
				else {
					
					
					//do nothing because you have to resolve it separate from the other words	
					
				
				}
				
				
			}
			
			//get the start of the linked list for one symbol
			for(int k=0; k<useList.size();k++){
				
				//gives us the location to look at the module
				int symIndex = useList.get(actualUseList[k]);
				
				String currentSymWord = currentWordList.get(symIndex);
				
				//the thing we will actually add to and change now 
				String address = currentSymWord.substring(0, currentSymWord.length()-1);
				
				int address2 = Integer.parseInt(address);
				
				
				address2 = address2 / 1000;
				
				address2 *= 1000;
				
				address2 += findLocation(actualUseList[k]);
				
				memoryMap.add(address2);
				
				//the address we will use to find the next word to change
				int nextAddress = Integer.parseInt(currentSymWord.substring(1, 
						currentSymWord.length()-1))%100;
				
				if(nextAddress == 77) {
					
					String newWord = currentWordList.get(symIndex);
					
					String newAddress = newWord.substring(0, newWord.length()-1);
					
					int cleanAddress = Integer.parseInt(newAddress);
					
					
					cleanAddress = cleanAddress / 1000;
					
					cleanAddress *= 1000;
					
					cleanAddress += findLocation(actualUseList[k]);
					
					memoryMap.add(address2);
				}
				
				else {
					
					System.out.println("do something");
					
				}
				
			}
			
		}
		
		System.out.println();
		//print out the memory map
		System.out.println("Memory Map");
		int counter = 0;
		
		for(int i=0; i<memoryMap.size(); i++) {
			
			System.out.print(counter+": ");
			System.out.println(memoryMap.get(i));
			counter++;
			
		}
		
		
	}
	
	
	public static int findLocation(String symbol) {
		
		for(int i=0; i<listOfModules.size();i++) {
			
			ArrayList<Symbol> symbolList = listOfModules.get(i).getSymbols();
			
			for(int j=0; j < symbolList.size(); j++ ) {
				
				if(symbolList.get(j).getVariable().equals(symbol)) {
					
					return symbolList.get(j).getRealAddress();
					
				}
				
			}
			
		}
		
		return 0;
		
		
	}
	
	
}

