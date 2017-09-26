public class Symbol {
	
	//create the data fields 
	private String variable; 
	private int address;
	private int realAddress;
	
	//constructor
	public Symbol(String variable, int address) {
		
		this.variable = variable;
		this.address = address;
		this.realAddress = 0;
	}

	//getter and setter methods
	public String getVariable() {
		return variable;
	}


	public void setVariable(String variable) {
		this.variable = variable;
	}


	public int getAddress() {
		return address;
	}
	
	public int getRealAddress(int baseAddress) {
		return (address + baseAddress);
	}


	public void setAddress(int address) {
		this.address = address;
	}

	

	public int getRealAddress() {
		return realAddress;
	}

	public void setRealAddress(int realAddress) {
		this.realAddress = realAddress;
	}

	public String toString(int baseAddress) {
		return variable + "=" + (address + baseAddress);
	}
	
	
	
	
}

