import json
from Models import RawMaterial
from Models import Product
from Models import Transformation
from _datetime import datetime
from web3 import Web3
from web3.middleware import geth_poa_middleware

baseURL = "http://127.0.0.1:22000"

# classe contente le istanze uniche dei filtri di tutti gli eventi che ci servono
class Filters(object):
    def __new__(cls, CFContract):
        if not hasattr(cls, "instance"):
            cls.instance = object.__new__(cls)
            cls.instance.transformation_events_filter = CFContract.events.newCFAdded().createFilter(fromBlock=0x0)
            cls.instance.raw_materials_isUsed_events_filter = CFContract.events.rawMaterialIsUsed().createFilter(fromBlock=0x0)
            cls.instance.is_finished_events_filter = CFContract.events.productIsFinished().createFilter(fromBlock=0x0)
            cls.instance.new_raw_material_lot_added_events_filter = CFContract.events.newRawMaterialLotAdded().createFilter(fromBlock=0x0)
            cls.instance.minted_products_events = CFContract.events.Transfer().createFilter(fromBlock=0x0)
        return cls.instance

# Funzione con istruzioni replicate per andare a connettersi alla blockchain
def connnectionUtils(URL):
    web3 = Web3(Web3.HTTPProvider(URL))
    abiUser = json.loads(
        '[{"inputs":[{"internalType":"address","name":"defaultSupplier","type":"address"},{"internalType":"address","name":"defaultTransformer","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"enum User.Role","name":"role","type":"uint8"}],"name":"newUser","type":"event"},{"inputs":[],"name":"CFaddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"carbon_fp","type":"uint16"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bool","name":"isEnded","type":"bool"}],"name":"addTransformation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"product_name","type":"string"},{"internalType":"uint256[]","name":"indexes","type":"uint256[]"}],"name":"createProduct","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string[]","name":"name","type":"string[]"},{"internalType":"uint256[]","name":"lot","type":"uint256[]"},{"internalType":"uint256[]","name":"cf","type":"uint256[]"}],"name":"createRawMaterials","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint8","name":"role","type":"uint8"}],"name":"createUser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"productId","type":"uint256"}],"name":"getProductById","outputs":[{"components":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"address","name":"currentOwner","type":"address"},{"internalType":"uint256","name":"CF","type":"uint256"},{"internalType":"bool","name":"ended","type":"bool"}],"internalType":"struct ProductLibrary.Product","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getProducts","outputs":[{"components":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"address","name":"currentOwner","type":"address"},{"internalType":"uint256","name":"CF","type":"uint256"},{"internalType":"bool","name":"ended","type":"bool"}],"internalType":"struct ProductLibrary.Product[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRawMaterials","outputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"lot","type":"uint256"},{"internalType":"address","name":"supplier","type":"address"},{"internalType":"uint256","name":"CF","type":"uint256"},{"internalType":"bool","name":"isUsed","type":"bool"}],"internalType":"struct ProductLibrary.RawMaterial[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getRole","outputs":[{"internalType":"enum User.Role","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRole","outputs":[{"internalType":"enum User.Role","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferCP","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
    abiCF = json.loads(
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"cf","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"pId","type":"uint256"}],"name":"newCFAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"string","name":"name","type":"string"},{"indexed":false,"internalType":"uint256","name":"lot","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"cf","type":"uint256"}],"name":"newRawMaterialLotAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"pId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"cf","type":"uint256"}],"name":"productIsFinished","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"transformer","type":"address"},{"indexed":false,"internalType":"address","name":"supplier","type":"address"},{"indexed":false,"internalType":"uint256","name":"pId","type":"uint256"},{"indexed":false,"internalType":"string","name":"name","type":"string"},{"indexed":false,"internalType":"uint256","name":"lot","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"cf","type":"uint256"}],"name":"rawMaterialIsUsed","type":"event"},{"inputs":[{"internalType":"uint256","name":"partialCF","type":"uint256"},{"internalType":"uint256","name":"pId","type":"uint256"},{"internalType":"bool","name":"isEnded","type":"bool"}],"name":"addCF","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string[]","name":"_rawMaterialName","type":"string[]"},{"internalType":"uint256[]","name":"_lot","type":"uint256[]"},{"internalType":"uint256[]","name":"_cf","type":"uint256[]"}],"name":"addRawMaterials","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAllProducts","outputs":[{"components":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"address","name":"currentOwner","type":"address"},{"internalType":"uint256","name":"CF","type":"uint256"},{"internalType":"bool","name":"ended","type":"bool"}],"internalType":"struct ProductLibrary.Product[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAllRawMaterials","outputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"lot","type":"uint256"},{"internalType":"address","name":"supplier","type":"address"},{"internalType":"uint256","name":"CF","type":"uint256"},{"internalType":"bool","name":"isUsed","type":"bool"}],"internalType":"struct ProductLibrary.RawMaterial[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"pId","type":"uint256"}],"name":"getProductById","outputs":[{"components":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"address","name":"currentOwner","type":"address"},{"internalType":"uint256","name":"CF","type":"uint256"},{"internalType":"bool","name":"ended","type":"bool"}],"internalType":"struct ProductLibrary.Product","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_productName","type":"string"},{"internalType":"uint256[]","name":"_index","type":"uint256[]"}],"name":"mintProduct","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"pId","type":"uint256"}],"name":"transferProduct","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
    address = web3.toChecksumAddress("0x8909F9F9c48BFc0945786A256623aF167fd05B5f")
    userContract = web3.eth.contract(address=address, abi=abiUser)
    addressCF = userContract.functions.CFaddress().call()
    CFContract = web3.eth.contract(address=addressCF, abi=abiCF)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3, CFContract, userContract


def convert_to_timestamp(event, web3) -> datetime:
    """This function convert a block timestamp into a datetime object

    :param event: event log retrieved from a block on the blockchain
    :type event: AttributeDict
    :param web3: instance of web3 connection to the blockchain
    :type web3: eth
    :return: datetime object containing the corresponding date of the timestamp
    :rtype: datetime
    """
    # Retrieving timestamp from the block where is saved event passed as parameter
    timestamp = web3.eth.getBlock(event['blockNumber'])['timestamp'] // 10**9
    # Converting timestamp in a standard date
    datetime.fromtimestamp(timestamp)
    return timestamp


def retrievingData(userContract, CFContract, filter_events, web3):
    """This function retrieves all data and events from the blockchain, required to construct array of products
    and rawmaterials, in local memory

    :param userContract: instance of contract that manages users
    :type userContract: Contract
    :param CFContract: instance of ERC721 contract that manages NFTs
    :type CFContract: Contract
    :param filter_events: instance of singleton containing all filters for blockchain events
    :type filter_events: Filters
    :param web3: instance of web3 connection to the blockchain
    :type web3: eth
    :return: two lists: The first is the products list and the second is the rawmaterials list
    """
    minted_products_events = filter_events.minted_products_events.get_all_entries()
    new_raw_material_lot_added_events = filter_events.new_raw_material_lot_added_events_filter.get_all_entries()
    # Retrieving and putting in a list all timestamps corresponding to the moments of insertions of rawmaterials
    time_of_insertions = [convert_to_timestamp(event, web3) for event in new_raw_material_lot_added_events]
    # initializing raw materials list with their attributes and times of insertion
    raw_materials_array = [RawMaterial.fromBlockChain(raw_material, time_of_insertion=t)
                           for raw_material, t in zip(userContract.functions.getRawMaterials().call(),
                                                      time_of_insertions)]
    # Creating products' list initializing attributes of all products as  come: ID, name, Owner,
    # current Carboon Footprint and time of start of the processing
    products_array = [Product.fromBlockChain(product, time_of_start=convert_to_timestamp(start_event, web3))
                      for product, start_event in zip(userContract.functions.getProducts().call(),
                                                      minted_products_events)]
    # Iterating over products' list in order to initialize other attributes as: raw materials' list, and
    # transformations' list. At the same time we add raw materials time of use only for consumed raw materials'
    # lots, since it is the same of processing time of start
    for product in products_array:
        # Retrieving all events about used raw materials
        raw_materials_events = CFContract.events.rawMaterialIsUsed().createFilter(fromBlock=0x0,
                                                                                  argument_filters={'pId': product.productId}
                                                                                  ).get_all_entries()
        # Retrieving all events about transformations
        transformations_events = CFContract.events.newCFAdded().createFilter(fromBlock=0x0,
                                                                             argument_filters={'pId': product.productId}
                                                                             ).get_all_entries()
        # Initializing transformation's list
        product_transformations = [Transformation(event['args']['userAddress'], event['args']['cf'],
                                                  convert_to_timestamp(event, web3))
                                   for event in transformations_events]
        # Retrieving the only event which certificates product's end of processing. If this event doesn't exist
        # we will get an empty list
        date_of_finishing = CFContract.events.productIsFinished().createFilter(fromBlock=0x0,
                                                                               argument_filters={'pId': product.productId}
                                                                               ).get_all_entries()
        # Retrieving all indexes of raw materials' used for current product from raw materials' list
        raw_materials_indexes = [raw_materials.index(RawMaterial(event['args']['name'],
                                                                 event['args']['lot'],
                                                                 event['args']['supplier'],
                                                                 event['args']['cf'])
                                                     ) for event in raw_materials_events]
        # Initializing list containing raw materials used for current product
        raw_materials_used = [raw_materials_array[raw_materials_indexes[i]]
                              for i in range(0, len(raw_materials_indexes))]
        # Adding time of use to raw materials using raw_materials_used list. This is possible, since elements in
        # raw-materials_used point to the same objects contained in raw materials list
        for raw in raw_materials_used:
            raw.time_of_use = product.time_of_start
        # Initializing product's list of raw materials using a copy of raw_materials_used in order to prevent
        # someone to modify raw materials list by acceding it from a product
        product.rawMaterials = raw_materials_used.copy()
        # Checking if product's processing is terminated e in that case updating end of processing date. We are
        # sure date_of_finishing will contain only an event since, when products are marked as finished on the
        # blockchain cannot be modified anymore
        if product.isEnded:
            product.time_of_finishing = datetime.fromtimestamp(web3.eth.getBlock(date_of_finishing[0]['blockNumber'])['timestamp'] // 10**9)
        # Initializing product's list of transformations using a copy of product_transformation in order to
        # prevent someone to modify product's transformation list by acceding it from this variable
        product.transformations = product_transformations.copy()
    return products, raw_materials


if __name__ == "__main__":
    web3, CFContractp, user_contract = connnectionUtils(baseURL)
    filters = Filters(CFContractp)
    products, raw_materials = retrievingData(user_contract, CFContractp, filters, web3)
    print(products[2])
    print(raw_materials[5])
    print(raw_materials[9])
    print(raw_materials[18])
