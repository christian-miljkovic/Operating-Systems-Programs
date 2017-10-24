import java.util.ArrayList;
import java.util.HashMap;

public class Module {
	private int baseAddress;
	private ArrayList<Symbol> symbols;
	private HashMap<String, Integer> useList;
	private ArrayList<String> word;

	public Module() {
		this.baseAddress = 0;
		this.symbols = new ArrayList<Symbol>();
		this.useList = new HashMap<String, Integer>();
		this.word = new ArrayList<String>();
	}

	public int getBaseAddress() {
		return this.baseAddress;
	}

	public void setBaseAddress(int baseAddress) {
		this.baseAddress = baseAddress;
	}

	public ArrayList<Symbol> getSymbols() {
		return this.symbols;
	}
	
	public Symbol getOneSymbol(int index) {
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
	
	public int getRealSymbolAddress(String sym, int baseAddress) {

		for (int i = 0; i < this.symbols.size(); i++) {
			if (sym.equals(this.symbols.get(i).getVariable())) {
				return this.symbols.get(i).getRealAddress(baseAddress);
			}
		}
		return 0;
	}
	
	public void setSymbols(Symbol symbols) {
		this.symbols.add(symbols);
	}

	public HashMap<String, Integer> getUseList() {
		return useList;
	}

	public void setUseList(String symbol, int loc) {
		this.useList.put(symbol,loc);
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
