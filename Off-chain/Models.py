
'''
Classe per la definizione del modello che devono avere i raw material.
Questa struttura permette di avere anche delle materie prime che derivano da 
più lotti nel caso in cui sia un caso che vorremo contemplare in futuro.
Ovviamente consente di avere anche più materie prime che derivano da un solo lotto
'''
from datetime import datetime

class RawMaterial:
    """
    Class mapping the structure of a raw material on the blockchain
    """
    def __init__(self, name: str, lot: int, address, cf: int, isUsed=False, time_of_insertion: datetime = None,
                 time_of_use: datetime = None):
        self.name = name
        self.lot = lot
        self.address = address
        self.cf = cf
        self.isUsed = isUsed
        self.time_of_insertion = time_of_insertion
        self.time_of_use = time_of_use

    @classmethod
    def fromBlockChain(cls, data: tuple, time_of_insertion=None, time_of_use=None):
        return cls(data[0], data[1], data[2], data[3], data[4], time_of_insertion, time_of_use)

    def __str__(self):
        return f"\t{self.name}\t{self.lot}\t{self.address}\t\t{self.cf}\t\t{self.time_of_insertion}\t\t{self.time_of_use}"
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, RawMaterial):
            return (self.name == __o.name) & (self.lot == __o.lot) & (self.address == __o.address)
        else:
            return False

class Product:
    """
    Class mapping the structure of a product on the blockchain
    """
    def __init__(self, productId: int, name: str, address, CF: int, isEnded=False, time_of_start: datetime=None,
                 time_of_finishing: datetime=None):
        self.productId = productId
        self.name = name
        self.address = address
        self.CF = CF
        self.isEnded = isEnded
        self.time_of_start = time_of_start
        self.time_of_finishing = time_of_finishing
        self.supplier = []
        self.transformations = []
        self.rawMaterials = []

    @classmethod
    def fromBlockChain(cls, data: tuple, time_of_start=None, time_of_finishing=None):
        return cls(data[0], data[1], data[2], data[3], data[4], time_of_start, time_of_finishing)

    def __str__(self):
        print(f"Information about product No. {self.productId}")
        print(f"Name:{self.name}, Owner:{self.address}, Actual Carboon Footprint:{self.CF}")
        print(f"Started on {self.time_of_start}")
        print('These are rawmaterials used for this product:')
        print()
        print('\tName\tlot\tsupplier\t\tCarboon Footprint\t\tDate of insertion\t\tDate of use')
        for raw in self.rawMaterials:
            print(raw)
        print('------------------------------------------------------------------------------')
        print('These are transformation done on this product:')
        print()
        print('\tAddress\t\tCarboon Footprint\t\tDate')
        for transformation in self.transformations:
            print(transformation)
        print('------------------------------------------------------------------------------')
        print()
        finished = f"Product was finished on {self.time_of_finishing}" if self.isEnded else "Product is still in the the works"
        return finished


class Transformation:
    """
    Class mapping the structure of a transformation operation recorded on a blockchain
    """
    def __init__(self, transformer, CF, date: datetime):
        self.transformer = transformer
        self.CF = CF
        self.date = date

    def __str__(self):
        return f"\t{self.transformer}\t{self.CF}\t{self.date}"
