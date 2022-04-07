from eth_typing import Address
from typing import List

import contracts
import event_logs
from functools import singledispatch
from Models import Product, RawMaterial, Transformation
from web3 import exceptions
from connection import web3


def set_account_as_default(user_role: int, address: Address) -> Address:
    """
    Function used to check if user address corresponds to the given role and set current user address as
    default web3 account in order to accomplish transactions
    Args:
        user_role: (int): the integer identifier of the role chose by the current user
        address: (Address): address of current logged user

    Returns:
        address: (Address): validated address of the current user

    Raises:
        Exception: Custom general error raised if a non planned error occurs

    """
    try:
        # Checking for correct account format
        account = web3.toChecksumAddress(address)
        # If the account is inside the list of known accounts of the block
        if account in web3.eth.accounts:
            web3.geth.personal.unlock_account(account, '')
            # Calling the method to check current account role inside user contract
            real_role = get_user_role()
            # If the account isnt registered inside the contract
            if real_role == 0 & user_role != 0:
                # The user is created with the given role inside the
                web3.eth.default_account = account
                contracts.user_contract.functions.createUser(user_role).transact()
            else:
                # The account is setted as the default account
                web3.eth.default_account = account
            return account
        # If the account isnt inside the current block's list of accounts
        else:
            # An error is raised
            raise Exception
    except Exception as e:
        raise Exception("Error: it's impossible to verify your role and address, please try again")


def get_user_role(address: Address=None) -> int:
    """
    Function used to validate user address and check if it corresponds to the given role. After
    validation function set the current user address as default web3 account in order to accomplish transactions
    Args:
        address: (Address): address of current logged user
    Returns:
        role: (int): role of current logged user
    """
    if address is None:
        return contracts.user_contract.functions.getRole().call()
    else:
        return contracts.user_contract.functions.getRole(address).call()


def create_raw_materials_on_blockchain(raw_materials):
    """Functions that inserts a new raw materials on the blockchain

    Args:
        raw_materials (`list[RawMaterial]`): List of raw materials that must be inserted
    """
    try:
        raw_materials_name_list = [raw_material.name for raw_material in raw_materials]
        raw_materials_lot_list = [raw_material.lot for raw_material in raw_materials]
        raw_materials_cf_list = [raw_material.cf for raw_material in raw_materials]
        contracts.user_contract.functions.createRawMaterials(raw_materials_name_list, raw_materials_lot_list,
                                                             raw_materials_cf_list).transact()

    except exceptions.SolidityError as e:
        # These are custom exceptions
        if (e.__str__ == "Il numero delle materie prime non corrisponde al numero di lotti") or (
                e.__str__ == "Il numero delle materie prime non corrisponde al numero delle carbon footprint") or (
                e.__str__ == "Hai già inserito questo lotto di questa materia prima"):
            print(e)
        # And these are other generic exceptions
        else:
            print(e)
            print("Errore nel caricamento delle materie prime, riprova")


def add_transformation_on_blockchain(carb_foot, product_id, is_the_final):
    """This function connects to the blockchain to add a new transformation
    
    Args:
        carb_foot (`int`): the value of the carbon footprint 
        product_id (`int`): the id of the product to which a new transformation needs to be added
        is_the_final (`bool`): boolean that indicates if this is the final transformation of the production chain
    
    Raises:
        `Exception`: if the operations fails
    """
    try:
        contracts.user_contract.functions.addTransformation(
            carb_foot, product_id, is_the_final).transact()
    except:
        raise Exception


def transfer_product_on_blockchain(transfer_to, product_id):
    """This function connects to the blockchain to transfer the ownership of a product
    
    Args:
        transfer_to (`ChecksumAddres`): the adress of the user to whom the product ownership needs to be transfered
        product_id (`int`): the id of the product to transfer

    Raises:
        `Exception`: if the operations fails
    """
    try:
        contracts.user_contract.functions.transferCP(transfer_to, product_id).transact()
    except Exception as e:
        raise e


def create_new_product_on_blockchain(product_name, raw_material_ids):
    """This function connects to the blockchain to add a new product
    
    Args:
        product_name (`str`): the name of the product to create
        raw_material_ids (`list[int]`): Ids of the raw materials to use for the product

    Raises:
        `Exception`: if the operations fails
    """
    try:
        contracts.user_contract.functions.createProduct(product_name, raw_material_ids).transact()
    except:
        raise Exception


def get_product(product_id: int) -> Product:
    """Gets the product from the blockchain with no informations on raw materials and transformations.

    Args:
        product_id (`int`): the id of the product to get

    Returns: 
        `Product`: a product from the blockchain
    """
    return Product.fromBlockChain(
        contracts.user_contract.functions.getProductById(product_id).call()
    )


# @singledispatch decorator allows function overloading depending on argument type
# (in this case argument is a Product Object)
# doc: https://docs.python.org/3/library/functools.html#functools.singledispatch
@singledispatch
def get_product_details(product: int) -> Product:
    """Gets information about raw material used and transformations performed on the specified product

    Args_
        product (`int`): the product id

    Returns
        `Product`: a product from the blockchain, with all of the info
    """
    # The information regarding the raw materials used and the transformations implemented
    # are taken from the events emitted on the blockchain
    rm_events = event_logs.get_raw_materials_used_events(product)
    transformation_events = event_logs.get_transformations_events(product)

    # The Product object is taken form the blockchain and the materials and transformation info is added
    product = get_product(product)
    product.rawMaterials = [RawMaterial.from_event(event=ev) for ev in rm_events]
    product.transformations = [
        Transformation.from_event(event=ev) for ev in transformation_events
    ]
    return product


@get_product_details.register
def _(product: Product) -> Product:
    """Overload of the `get_product_details` function.
    Gets informations about raw material used and transformations performed on the specified product.
    
    Args:
        product (`Product`): the product object without the requested info

    Returns:
        `Product`: a product from the blockchain, with all of the info
    """
    # The info regarding the raw materials used and the transformations implemented
    # are taken from the events emitted on the blockchain
    rm_events = event_logs.get_raw_materials_used_events(product.productId)
    transformation_events = event_logs.get_transformations_events(product.productId)

    # materials and transformation info is added to the product
    product.rawMaterials = [RawMaterial.from_event(event=ev) for ev in rm_events]
    product.transformations = [
        Transformation.from_event(event=ev) for ev in transformation_events
    ]
    return product


def get_raw_material_not_used() -> List[RawMaterial]:
    """This function fetches and returns a list of non-used raw materials from the blockchain
    
    Returns:
        `list[RawMaterial]`: a list of all of the non-used raw materials
    """
    rms = list(filter(lambda e: e.isUsed == False, get_all_raw_materials()))
    return rms


def get_all_raw_materials() -> List[RawMaterial]:
    """This function fetches and returns the list of all of the raw materials saved on the blockchain
    
    Returns:
        `list[RawMaterial]`: a list of all of the raw materials    
    """
    return [
        RawMaterial.fromBlockChain(rm)
        for rm in contracts.user_contract.functions.getRawMaterials().call()
    ]


def get_all_products() -> List[Product]:
    """
    Retrieves all `Product`s on the blockchain.
    This function returns a list of all the products without informations
    about raw materials used or transformations.

    If you need these information for a specific product, use
    `get_product_details`, or if you need them for all products use
    `get_all_products_detailed`


    Returns: 
        `list[Product]`: a list of all the products on the blockchain
    """
    return [
        Product.fromBlockChain(product)
        for product in contracts.user_contract.functions.getProducts().call()
    ]


# uguale alla precedente get_products_from_blockchain()
# o visto che non salviamo i dati ora non so se ha senso il 'from_blockchain' vedete voi come è meglio
'''
def get_all_products_detailed() -> list[Product]:
    """
    Retrieves all `Product`s on the blockchain with informations on raw
    materials and transformation.

    Returns:
    `list[Product]`: a list of all the products on the blockchain
    """
    return [get_product_details(product) for product in get_all_products()]


# È utile a qualcosa?
def get_transferred_products():
    pass

# uguale alla precedente get_raw_materials_from_blockchain()
# visto che non salviamo i dati ora non so se ha senso il 'from_blockchain' vedete voi come è meglio


'''
