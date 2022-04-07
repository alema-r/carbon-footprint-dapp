import inquirer
import re

from web3 import Web3

from Models import Product
from BlockChain import add_transformation_on_blockchain, transfer_product_on_blockchain, create_new_product_on_blockchain, get_raw_material_not_used, get_all_products
from Utils import carbon_fp_input_validation, address_validation
from Models import RawMaterial


def get_updatable_user_products(user_address):
    '''This function filters the products stored in the blockhain. It returns a list of the products that are owned by the 
    current user.

    Args:
        products (`List[Product]`): the list of the products stored in the blockhain
        user_address (`ChecksumAddress`): the adress of the current user

    Returns:
        `list[Product]`: the list of the products owned by the current user
    '''
    all_products = get_all_products()
    return list(filter(lambda p: (p.address == user_address and not p.isEnded), all_products))


def new_product_name_input_validation(answers, current):
    '''This function validates a name of a product.

    Args:
        answers
        current

    Returns:
        `True`: if the name is valid

    Raises:
        `ValidationError`: if the name is invalid
    '''
    pattern = "^[a-zA-Z0-9 ]*$"
    if bool(re.match(pattern, current.strip(' '))) and len(current) > 0:
        return True
    else:
        raise inquirer.errors.ValidationError('', reason=f'Invalid input: Product\'s name is invalid. Please insert \
        names with only letters and numbers or type almost one character')


def add_transformation(user_address):
    '''This function lets the transformer user add a new trasformation to the production chain of a product that they own. 

    Args:
        user_address(`ChecksumAddress`): the address of the current user
    '''
    #gets the products associated with the current user
    user_products = get_updatable_user_products(user_address)
    product_id = inquirer.list_input(
        message="What product do you want to update?",
        choices=[(product.name, product.productId) for product in user_products]
    )

    #asks the user for the carbon footprint of the transformation
    carb_footprint = inquirer.text(
        message="Insert the carbon footprint value of this transformation: ",
        validate=carbon_fp_input_validation
    )

    #asks the user if this is the final transformation of the selected product
    is_final = inquirer.confirm(
        message="Is this the final transformation?"
    )

    #asks the user for confirmation
    confirm = inquirer.confirm(
        message=f"Do you want to add this transformation, with a carbon footprint of {carb_footprint}, to the selected \
        product? BE CAREFUL, after this operation the product will be no longer modifiable" if is_final else f"Do you \
        Do you want to add this transformation, with a carbon footprint of {carb_footprint}, to the selected product?"
    )

    #if the user confirms the transaction is started.
    if confirm:
        try:
            add_transformation_on_blockchain(
                int(carb_footprint), product_id, is_final)
        except Exception as e:
            print(e)
            print(
                "Something went wrong while trying to add the transformation to the blockchain... Please retry.")


def transfer_product(user_address):
    '''This function lets the transformer user transfer the property of a product to another transformer

    Args:
        user_address (`ChecksumAddress`): the list of the products that the user currently owns
    '''
    # get products associated with user address
    user_products = get_updatable_user_products(user_address)

    product_id = inquirer.list_input(
        message="What product do you want to transfer? ",
        choices=[(product.name, product.productId) for product in user_products]
    )

    address_ok = False
    #RIVEDERE
    while not address_ok:
        transfer_to = inquirer.text(
            message="Insert the address of the transformer to who you want to transfer the product: ",
        )
        address_ok, checked_address = address_validation(transfer_to, 2)
        if not address_ok:
            print("The specified address is not valid, please retry.")
    
    #asks the user for confirmation
    confirm = inquirer.confirm(
        message=f"Do you want to transfer the selected product to the address {transfer_to}?"
    )

    #if the user confirms the transaction is started.
    if confirm:
        try:
            transfer_product_on_blockchain(checked_address, product_id)
        except Exception as e:
            print(e)
            print(
                "Something went wrong while trying to trasfer the ownership of the product... Please retry.")


def create_new_product():
    """This function lets the transformer create a new product, by selecting the necessary raw materials"""

    #asks the name of the product
    product_name = inquirer.text(
        message="Type the name of the product you want to create: ",
        validate=new_product_name_input_validation
    )

    #The user selects the raw materials to use.
    raw_materials = get_raw_material_not_used()
    raw_materials_to_use = inquirer.checkbox(
        message="Select a raw material to use",
        choices=[(material.__str__(), material.materialId) for material in raw_materials]
    )

    #asks the user for confirmation
    confirm = inquirer.confirm(
        message=f'Do you want to create the product "{product_name} with the selected materials?'
    )

    #if the user confirms the transaction is started.
    if confirm:
        try:
            create_new_product_on_blockchain(
                product_name, raw_materials_to_use)
        except Exception as e:
            print(e)
            print("Please insert the new product again...")
