import json

class SymbolTranslate():
    def __init__(self) -> None:
        symbol_table_file = open('./symbol-file.json', 'r', encoding='utf-8')
        self.symbol_table = json.load(symbol_table_file)
        print(self.symbol_table)
        symbol_table_file.close()

    def get_symbol_table(self):
        return self.symbol_table
    
class senakps_file_handler():
    def __init__(self) -> None:
        record_file = open('./record.senakps', 'r', encoding='utf-8')