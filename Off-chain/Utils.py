from cmath import nan
import inquirer

def lot_input_validation(answers, current):
    try:
        int_cf=int(current)
    except:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Lot must be positive integer')
    if int_cf < 0:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Lot must be positive integer')
    return True

'''
Funzione che fa tutte le validazioni che richiedono un confronto fra materie prime e lotti.
'''
def input_validation(raw_material, raw_materials):
    # Controlla cha la materia prima e il lotto associato non siano già stati inseriti nei precedenti passaggi
    # Questo controllo funziona solo se tra materia prima e lotto c'è una corrispondenza uno a uno, che credo fosse il nostro caso
    # TODO: controllare anche con le materie prime che gia stanno sulla blockchain
    if raw_material in raw_materials:
        error_message = "Raw material and lot already inserted"
        return False, error_message
    
    return True, ''


def address_validation(answers, current):
    #TODO: do address validation and check
    return True

'''
Funzione che controlla il corretto formato numerico della carbon footprint inserita dall'utente
'''
def carbon_fp_input_validation(answers, current):
    try:
        int_cf=int(current)
    except:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Carbon footprint must be positive integer')
    if int_cf < 0:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Carbon footprint must be positive integer')
    return True

def raw_material_name_input_validation(answers, current):
    special_characters = "!@#$%^&*()-+?_=,<>\""
    if any(c in special_characters for c in current):
        raise inquirer.errors.ValidationError('', reason= 'Invalid input: Product\'s name can not contain special characters')    
    if len(current) == 0:
        raise inquirer.errors.ValidationError('', reason= 'Invalid input: Product\'s name can not be empty')    
    return True

'''
Classe per la definizione del modello che devono avere i raw material.
Questa struttura permette di avere anche delle materie prime che derivano da 
più lotti nel caso in cui sia un caso che vorremo contemplare in futuro.
Ovviamente consente di avere anche più materie prime che derivano da un solo lotto
'''
 
class Raw_material:
    def __init__(self, name: str, lot: int, address, cf: int):
        self.__name = name
        self.__lot = lot
        self.__address = address
        self.__cf = cf
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Raw_material):
            return ((self.__name == __o.__name) & (self.__lot == __o.__lot) & (self.__address == __o.__address))
        else:
            return False

    
    def set_name(self, name: str):
        self.__name = name

    def set_lot(self, lot: int):
        self.__lot = lot

    def set_cf(self, cf: int):
        self.__cf = cf
        
    def get_name(self):
        return self.__name

    def get_lot(self):
        return self.__lot

    def get_address(self):
        return self.__address

    def get_cf(self):
        return self.__cf