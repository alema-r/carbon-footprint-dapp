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

    def __init__(self, name: str, lot: int, address, cf: int, isUsed=False, materialId: int = None ,time_of_insertion: datetime = None,
                 time_of_use: datetime = None):
        self.materialId = materialId
        self.name = name
        self.lot = lot
        self.address = address
        self.cf = cf
        self.isUsed = isUsed
        self.time_of_insertion = time_of_insertion
        self.time_of_use = time_of_use

    @classmethod
    def fromBlockChain(cls, data: tuple, time_of_insertion=None, time_of_use=None):
        return cls(data[1], data[2], data[3], data[4], data[5], data[0], time_of_insertion, time_of_use)

    def from_event(event, used=False):
        return RawMaterial(event.args.name, event.args.lot, event.args.supplier, event.args.cf, used)#, event.args.materialId)

    def __str__(self):
        return f"{self.name}\t{self.lot}\t{self.address}\t{self.cf}"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, RawMaterial):
            return (self.materialId == __o.materialId) & (self.name == __o.name) & (self.lot == __o.lot) & (self.address == __o.address)
        else:
            return False


class Product:
    """
    Class mapping the structure of a product on the blockchain
    """
    def __init__(self, productId: int, name: str, address, CF: int, isEnded=False):
        self.productId = productId
        self.name = name
        self.address = address
        self.CF = CF
        self.isEnded = isEnded
        self.supplier = []
        self.transformations = []
        self.rawMaterials = []

    @classmethod
    def fromBlockChain(cls, data: tuple, time_of_start=None, time_of_finishing=None):
        return cls(data[0], data[1], data[2], data[3], data[4])

    def __str__(self):
        print(f"Information about product No. {self.productId}")
        print(f"Name:{self.name}, Owner:{self.address}, Actual Carboon Footprint:{self.CF}")
        print('These are rawmaterials used for this product:')
        print()
        print(
            '\tName\tlot\tsupplier\t\tCarboon Footprint\t\tDate of insertion\t\tDate of use')
        for raw in self.rawMaterials:
            print(raw)
        print(
            '------------------------------------------------------------------------------')
        print('These are transformation done on this product:')
        print()
        print('\tAddress\t\tCarboon Footprint\t\tDate')
        for transformation in self.transformations:
            print(transformation)
        print(
            '------------------------------------------------------------------------------')
        print()
        finished = f"Product is finished" if self.isEnded else "Product is still in the works"
        return finished


class Transformation:
    """
    Class mapping the structure of a transformation operation recorded on a blockchain
    """

    def __init__(self, transformer, CF, date: datetime = None):
        self.transformer = transformer
        self.CF = CF
        self.date = date

    def from_event(event):
        return Transformation(event.args.userAddress, event.args.cf)

    def __str__(self):
        return f"{self.transformer}\t{self.CF}\t{self.date}"
