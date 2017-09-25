package homework01_202;

public class Symbol {
	
	//create the data fields 
	private String variable; 
	private int address;
	
	//constructor
	public Symbol(String variable, int address) {
		
		this.variable = variable;
		this.address = address;
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


	public void setAddress(int address) {
		this.address = address;
	}


	@Override
	public String toString() {
		return variable + "=" + address;
	}
	
	
}
