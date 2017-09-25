package homework01_202;
import java.util.ArrayList;

public class Module {
	private int baseAddress;
	private ArrayList<Symbol> symbols;
	private ArrayList<String> useList;
	private ArrayList<String> word;

	public Module() {
		this.baseAddress = 0;
		this.symbols = new ArrayList<Symbol>();
		this.useList = new ArrayList<String>();
		this.word = new ArrayList<String>();
	}

	public int getBaseAddress() {
		return this.baseAddress;
	}

	public void setBaseAddress(int baseAddress) {
		this.baseAddress = baseAddress;
	}

	public Symbol getSymbols(int index) {
		return this.symbols.get(index);
	}
	
	public int getSymbolAddress(String sym) {

		for (int i = 0; i < this.symbols.size(); i++) {
			if (sym.equals(this.symbols.get(i).getVariable())) {
				return this.symbols.get(i).getAddress();
			}
		}
		return 0;
	}
	
	public void setSymbols(Symbol symbols) {
		this.symbols.add(symbols);
	}

	public ArrayList<String> getUseList() {
		return useList;
	}

	public void setUseList(String useList) {
		this.useList.add(useList);
	}

	public ArrayList<String> getWord() {
		return word;
	}

	public void setWord(String word) {
		this.word.add(word);
	}

	@Override
	public String toString() {
		return "Module [baseAddress=" + baseAddress + ", symbols=" + symbols + ", useList=" + useList + ", word=" + word
				+ "]";
	}
	
	
	
	
	
	
}
