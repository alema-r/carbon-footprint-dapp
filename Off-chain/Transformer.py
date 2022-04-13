from re import S
from unicodedata import name
import inquirer
from numpy import product
from BlockChain import add_transformation_on_blockchain, transfer_product_on_blockchain, create_new_product_on_blockchain, get_raw_material_not_used, get_all_products
import validation
from web3 import Web3


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
    return list(filter(lambda p: (p.address == user_address and not p.is_ended), all_products))


def add_transformation(user_address):
    '''This function lets the transformer user add a new trasformation to the production chain of a product that they own. 

    Args:
        user_address(`ChecksumAddress`): the address of the current user
    '''
    # gets the products associated with the current user
    user_products = get_updatable_user_products(user_address)
    product_id = inquirer.list_input(
        message="What product do you want to update?",
        choices=[(product.name, product.product_id)
                 for product in user_products]
    )

    # asks the user for the carbon footprint of the transformation
    carb_footprint = inquirer.text(
        message="Insert the carbon footprint value of this transformation: ",
        validate=validation.carbon_fp_input_validation
    )

    # asks the user if this is the final transformation of the selected product
    is_final = inquirer.confirm(
        message="Is this the final transformation?"
    )

    # asks the user for confirmation
    if is_final:
        print("BE CAREFUL, after this operation the product will be no longer modifiable")
    confirm = inquirer.confirm(
        message=f"Do you want to add this transformation, with a carbon footprint of {carb_footprint}, to the selected product?"
    )

    # if the user confirms the transaction is started.
    if confirm:
        success = add_transformation_on_blockchain(
            int(carb_footprint), product_id, is_final)
        if success:
            print("Operation completed successfully")


def transfer_product(user_address):
    '''This function lets the transformer user transfer the property of a product to another transformer

    Args:
        user_address (`ChecksumAddress`): the list of the products that the user currently owns
    '''
    # get products associated with user address
    user_products = get_updatable_user_products(user_address)

    product_id = inquirer.list_input(
        message="What product do you want to transfer? ",
        choices=[(product.name[:22]+"..." if len(product.name > 25)
                  else product.name, product.product_id) for product in user_products]
    )

    transfer_to = inquirer.text(
        message="Insert the address of the transformer to who you want to transfer the product: ",
        validate=validation.transformer_address_validation
    )
    # asks the user for confirmation
    confirm = inquirer.confirm(
        message=f"Do you want to transfer the selected product to the address {transfer_to}?"
    )

    # if the user confirms the transaction is started.
    if confirm:
        success = transfer_product_on_blockchain(
            Web3.toChecksumAddress(transfer_to), product_id)
        if success:
            print("Operation completed succesfully")


def create_new_product():
    """This function lets the transformer create a new product, by selecting the necessary raw materials"""

    # asks the name of the product
    product_name = inquirer.text(
        message="Type the name of the product you want to create: ",
        validate=validation.name_input_validation
    )

    # The user selects the raw materials to use.
    raw_materials = get_raw_material_not_used()
    raw_materials_to_use = inquirer.checkbox(
        message="Select a raw material to use",
        choices=[(material.__str__(), material.material_id)
                 for material in raw_materials]
    )

    # asks the user for confirmation
    confirm = inquirer.confirm(
        message=f'Do you want to create the product "{product_name}" with the selected materials?'
    )

    # if the user confirms the transaction is started.
    if confirm:
        success = create_new_product_on_blockchain(
            product_name, raw_materials_to_use)
        if success:
            print("Operation completed successfully")
