
'''
Classe per la definizione del modello che devono avere i raw material.
Questa struttura permette di avere anche delle materie prime che derivano da 
più lotti nel caso in cui sia un caso che vorremo contemplare in futuro.
Ovviamente consente di avere anche più materie prime che derivano da un solo lotto
'''
 
class Raw_material:
    def __init__(self, name: str, lot: int, address, cf: int, isEnded = False ):
        self.__name = name
        self.__lot = lot
        self.__address = address
        self.__cf = cf
        self.__isEnded = isEnded
    
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
    
    def set_isEnded(self, isEnded: bool):
        if (self.__isEnded == False):
            self.__isEnded = isEnded
        
    def get_name(self):
        return self.__name

    def get_lot(self):
        return self.__lot

    def get_address(self):
        return self.__address

    def get_cf(self):
        return self.__cf
    
    def get_isEnded(self):
        return self.__isEnded