from eth_typing import Address
import contracts
import event_logs
from functools import singledispatch
from Models import Product, RawMaterial, Transformation
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3 import exceptions

BASE_URL = "http://127.0.0.1:2200"


def connect(role: int, address:Address) -> Web3:
    url = BASE_URL + str(role)
    try:
        # Tring to connect to blockchain
        web3 = Web3(Web3.HTTPProvider(url))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        # Checking for correct account format
        account = web3.toChecksumAddress(address)
        # If the account is inside the list of known accounts of the block
        if account in web3.eth.accounts:
            # Calling the method to ckeck current account role inside user contract
            real_role = contracts.user_contract.functions.getRole(account).call()
            # If the account isnt registered inside the contract 
            if real_role == 0:
                # The user is created with the given role inside the contract
                contracts.user_contract.functions.createUser(role).transact()
            # The account is setted as the default account
            web3.default_account = account
        # If the account isnt inside the current block's list of accounts
        else:
            # An error is raised
            raise Exception
    except:
        raise Exception("Error: it's impossible to verify your role and address, please try again")
    return web3


def create_raw_materials_on_blockchain(raw_materials):
    """Functions that insert new raw materials on blockchain

    Args:
        contract (Contract): User contract address used to call his functions
        raw_materials (List[RawMaterial]): List of raw materials that must be inserted

    Raises:
        e: Error returned from Blockchain
        Exception: Custom general error raised if a non planned error occurs
    """
    try:
        raw_materials_name_list = [raw_material.name for raw_material in raw_materials]
        raw_materials_lot_list = [raw_material.lot for raw_material in raw_materials]
        raw_materials_cf_list = [raw_material.cf for raw_material in raw_materials]
        contracts.user_contract.functions.createRawMaterials(raw_materials_name_list, raw_materials_lot_list, raw_materials_cf_list).transact()
    except exceptions.SolidityError as e:
        if (e.__str__ == "Il numero delle materie prime non corrisponde al numero di lotti") or (e.__str__ == "Il numero delle materie prime non corrisponde al numero delle carbon footprint") or (e.__str__ == "Hai già inserito questo lotto di questa materia prima"):
            print(e)
        else:
            print("Errore nel caricamento delle materie prime, riprova")

def transfer_cp(recipient, token_id):
    try:
        # Funzione che trasferisce la CP al trasformatore.
        contracts.user_contract.functions.transferCP(recipient, token_id).transact()
    except:
        raise Exception("Token transfer error")

def add_transformation_on_blockchain(carb_foot, product_id, is_the_final):
    '''This function connects to the blockchain to add a new transformation
    
    Keyword arguments:
    contract -- the instance of Contract needed to connect to the blockchain
    carb_foot -- the value of the carbon footprint 
    product_id -- the id of the product to which a new transformation needs to be added
    is_the_final -- boolean that indicates if this is the final transformation of the production chain'''
    try:
        contracts.user_contract.functions.addTransformation(
            carb_foot,  product_id, is_the_final).transact()
    except:
        raise Exception
        
def transfer_product_on_blockchain(transfer_to, product_id):
    '''This function connects to the blockchain to transfer the ownership of a product
    
    Keyword arguments:
    contract -- the instance of Contract needed to connect to the blockchain
    transfer_to -- the adress of the user to whom the product ownership needs to be transfered
    product_id -- the id of the product to transfer
    '''
    try:
        contracts.user_contract.functions.transferCP(transfer_to, product_id).transact()
    except:
        raise Exception


def create_new_product_on_blockchain(product_name, raw_material_indexes):
    """This function connects to the blockchain to add a new product"""
    try:
        contracts.user_contract.functions.createProduct(product_name,raw_material_indexes)
    except:
        raise Exception



def get_product(product_id: int) -> Product:
    """Gets the product from the blockchain with no informations on 
    raw materials and transformations.
    :param product_id: the id of the product to get
    :type product_id: int
    :returns: a product from the blockchain
    :rtype: Product
    """
    return Product.fromBlockChain(
        contracts.user_contract.functions.getProductById(product_id).call()
    )


# Il decoratore singledispatch permette di fare function overloading in base al
# tipo di argomento (in questo caso l'argomento product)
# doc: https://docs.python.org/3/library/functools.html#functools.singledispatch
@singledispatch
def get_product_details(product: int) -> Product:
    """Gets informations about raw material used and transformations performed
    on the specified product
    :param product: the product id
    :type product: int
    :returns: a Product object
    :rtype: Product
    """
    rm_events = event_logs.get_raw_materials_used_events(product)
    transformation_events = event_logs.get_transformations_events(product)
    product = get_product(product)
    product.rawMaterials = [RawMaterial.from_event(event=ev) for ev in rm_events]
    product.transformations = [
        Transformation.from_event(event=ev) for ev in transformation_events
    ]
    return product


@get_product_details.register
def _(product: Product) -> Product:
    """Overload of the `get_product_details` function.
    Gets informations about raw material used and transformations performed
    on the specified product.
    :param product: the product object 
    :type product: Product
    :returns: a Product object
    :rtype: Product
    """
    rm_events = event_logs.get_raw_materials_used_events(product.productId)
    transformation_events = event_logs.get_transformations_events(product.productId)
    product.rawMaterials = [RawMaterial.from_event(event=ev) for ev in rm_events]
    product.transformations = [
        Transformation.from_event(event=ev) for ev in transformation_events
    ]
    return product

# uguale alla precedente get_products_from_blockchain()
#o visto che non salviamo i dati ora non so se ha senso il 'from_blockchain' vedete voi come è meglio

def get_all_products() -> list[Product]:
    """
    Retrieves all `Product`s on the blockchain.
    This function returns a list of all the products without informations
    about raw materials used or transformations.

    If you need these information for a specific product, use
    `get_product_details`, or if you need them for all products use
    `get_all_products_detailed`
    :returns: a list of all the products on the blockchain
    :rtype: list
    """
    return [
        Product.fromBlockChain(product)
        for product in contracts.user_contract.functions.getProducts().call()
    ]


def get_all_products_detailed() -> list[Product]:
    """
    Retrieves all `Product`s on the blockchain with informations on raw
    materials and transformation.
    :returns: a list of all the products on the blockchain
    :rtype: list
    """
    return [get_product_details(product) for product in get_all_products()]


# È utile a qualcosa?
def get_transferred_products():
    pass

# uguale alla precedente get_raw_materials_from_blockchain()
# visto che non salviamo i dati ora non so se ha senso il 'from_blockchain' vedete voi come è meglio
def get_all_raw_materials() -> list[RawMaterial]:
    return [
        RawMaterial.fromBlockChain(rm)
        for rm in contracts.user_contract.functions.getRawMaterials().call()
    ]


def get_raw_material_not_used() -> list[RawMaterial]:
    rms = list(filter(lambda e: e[4] == False, get_all_raw_materials()))
    return [RawMaterial.fromBlockChain(rm) for rm in rms]
