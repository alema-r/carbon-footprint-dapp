
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
    def from_blockchain(cls, data: tuple):
        """
        Alternative constructor of RawMaterial class in order to simply instantiate objects with data retrieved from
        blockchain
        Args:
            data: (tuple) structure returned after calling smart contracts

        Returns:
            RawMaterial Object
        """
        return cls(data[1], data[2], data[3], data[4], data[5], data[0])

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
        if len(self.name) < 25:
            length = len(self.name)
            padding = ''.join([' ' for i in range(length, 30)])
            name = self.name + padding
        else:
            padding = ''.join([' ' for i in range(0, 5)])
            name = self.name + padding
        if len(str(self.lot)) < 6:
            padding = "".join([' ' for i in range(len(str(self.lot)), 6)])
            lot = str(self.lot) + padding
        else:
            padding = "".join([' ' for i in range(0, 3)])
            lot = str(self.lot) + padding
        if len(str(self.cf)) < 6:
            padding = "".join([' ' for i in range(len(str(self.cf)), 6)])
            cf = str(self.cf) + padding
        else:
            padding = "".join([' ' for i in range(0, 3)])
            cf = str(self.cf) + padding
        return f"{name}{lot}{cf}{self.address}"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, RawMaterial):
            return (self.material_id == __o.material_id) and (self.name == __o.name) and (self.lot == __o.lot) and \
                   (self.address == __o.address)
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
    def from_blockchain(cls, data: tuple):
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
        raw_materials_printable = [[raw.name, raw.lot, raw.cf, raw.address] for raw in self.rawMaterials]
        table_raw_materials = tabulate(raw_materials_printable, headers=['Name', 'Lot', 'Carbon Footprint', 'Supplier'],
                                       tablefmt='tsv')
        transformations_printable = [[t.cf, t.transformer] for t in self.transformations]
        table_transformation = tabulate(transformations_printable, headers=['Carbon Footprint', 'Transformer'],
                                        tablefmt='tsv')
        s = f"Information about product No. {self.product_id}\nOwner: {self.address}\n" +\
            f"Name:{self.name}, Actual Carbon Footprint:{self.cf}\n" +\
            "These are raw materials used for this product:\n\n" + table_raw_materials + \
            "\n\n------------------------------------------------------------------------------\n\n" + \
            "These are transformation done on this product:\n" + table_transformation + \
            "\n\n------------------------------------------------------------------------------\n\n"
        s += f"Product is finished\n" if self.is_ended else "Product is still in the works\n"
        return s


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

        Returns:
            RawMaterial Object
        """
        return cls(event.args.userAddress, event.args.cf)

    def __str__(self):
        return f"{self.cf}\t{self.transformer}"
