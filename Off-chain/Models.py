'''
Classe per la definizione del modello che devono avere i raw material.
Questa struttura permette di avere anche delle materie prime che derivano da
più lotti nel caso in cui sia un caso che vorremo contemplare in futuro.
Ovviamente consente di avere anche più materie prime che derivano da un solo lotto
'''
from datetime import datetime
from tabulate import tabulate
from web3.datastructures import AttributeDict


class RawMaterial:
    """
    Class mapping the structure of a raw material on the blockchain
    """

    def __init__(self, name: str, lot: int, address, cf: int, is_used=False, material_id: int = None):
        self.material_id = material_id
        self.name = name
        self.lot = lot
        self.address = address
        self.cf = cf
        self.is_used = is_used

    @classmethod
    def fromBlockChain(cls, data: tuple, time_of_insertion=None, time_of_use=None):
        """
        Alternative constructor of RawMaterial class in order to simply instantiate objects with data retrieved from
        blockchain
        Args:
            data: (tuple) structure returned after calling smart contracts
            time_of_insertion:
            time_of_use:

        Returns:
            RawMaterial Object
        """
        return cls(data[1], data[2], data[3], data[4], data[5], data[0], time_of_insertion, time_of_use)

    @classmethod
    def from_event(cls, event: AttributeDict, used=False):
        """
        Alternative constructor of RawMaterial class in order to simply instantiate objects with data about events
        retrieved from blockchain
        Args:
            event: (AttributeDict) dictionary containing event logs returned from blockchain
            used: (bool) boolean parameter indicating whether raw material is used or not

        Returns:
            RawMaterial Object
        """
        return cls(event.args.name, event.args.lot, event.args.supplier, event.args.cf, used)

    def __str__(self):
        return f"{self.name}\t{self.lot}\t{self.cf}\t{self.address}"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, RawMaterial):
            return (self.materialId == __o.materialId) and (self.name == __o.name) and (self.lot == __o.lot) and (self.address == __o.address)
        else:
            return False


class Product:
    """
    Class mapping the structure of a product on the blockchain
    """
    def __init__(self, product_id: int, name: str, address, cf: int, is_ended=False):
        self.product_id = product_id
        self.name = name
        self.address = address
        self.cf = cf
        self.is_ended = is_ended
        self.transformations = []
        self.rawMaterials = []

    @classmethod
    def fromBlockChain(cls, data: tuple):
        """
        Alternative constructor of Product class in order to simply instantiate objects with data retrieved from
        blockchain
        Args:
            data: (tuple) structure returned after calling smart contracts
        Returns:
            Product Object
        """
        return cls(data[0], data[1], data[2], data[3], data[4])

    def __str__(self):
        print(f"Information about product No. {self.productId}")
        print(f"Owner: {self.address}")
        print(f"Name:{self.name}, Actual Carboon Footprint:{self.CF}")
        print('These are raw materials used for this product:')
        print()
        raw_materials_printable = [[raw.name, raw.lot, raw.cf, raw.address] for raw in self.rawMaterials]
        table = tabulate(raw_materials_printable, headers=['Name', 'Lot', 'Carboon Footprint', 'Supplier'],
                         tablefmt='tsv')
        print(table)
        print('------------------------------------------------------------------------------')
        print('These are transformation done on this product:')
        print()
        transformations_printable =[[t.CF, t.transformer] for t in self.transformations]
        table = tabulate(transformations_printable, headers=['Carboon Footprint', 'Transformer'],
                         tablefmt='tsv')
        print(table)
        print('------------------------------------------------------------------------------')
        print()
        finished = f"Product is finished" if self.isEnded else "Product is still in the works"
        return finished


class Transformation:
    """
    Class mapping the structure of a transformation operation recorded on a blockchain
    """

    def __init__(self, transformer, cf):
        self.transformer = transformer
        self.cf = cf

    @classmethod
    def from_event(cls, event: AttributeDict):
        """
        Alternative constructor of Transformation class in order to simply instantiate objects with data about events
        retrieved from blockchain
        Args:
            event: (AttributeDict) dictionary containing event logs returned from blockchain
            used: (bool) boolean parameter indicating whether raw material is used or not

        Returns:
            RawMaterial Object
        """
        return cls(event.args.userAddress, event.args.cf)

    def __str__(self):
        return f"{self.cf}\t{self.transformer}"
