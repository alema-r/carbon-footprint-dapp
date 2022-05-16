"""Module that implements a view for the transformer
"""
import inquirer
from inquirer.themes import load_theme_from_dict
from requests import exceptions as requests_exceptions
from web3 import Web3

from off_chain.controller_transformer import Transformer
from off_chain.theme_dict import theme
from off_chain import validation


def add_transformation(web3: Web3):
    """This function lets the transformer user add a new transformation
    to the production chain of a product that they own.

    Args:
        web3 (Web3): used to access the address of the current user
    """
    try:
        transformer = Transformer(web3)
    except requests_exceptions.ConnectionError:
        print("Could not connect to the blockchain. Try again")
        return
    # gets the products associated with the current user
    user_products = transformer.get_updatable_user_products(web3.eth.default_account)

    if len(user_products) == 0:
        print("You don't have any product to update\n")
        return

    print(
        "Follow the instructions to add a transformation to a product."
        "You can cancel operation in any moment by pressing Ctrl+C"
    )

    questions = [
        inquirer.List(
            "product_id",
            message="What product do you want to update?",
            choices=[
                (str(product.product_id) + " - " + product.name, product.product_id)
                for product in user_products
            ],
            carousel=True,
        ),
        inquirer.Text(
            "CF",
            message="Insert the carbon footprint value of this transformation",
            validate=validation.carbon_fp_input_validation,
        ),
        inquirer.Confirm(
            "final",
            message="Is this the final transformation?",
        ),
    ]
    answers = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if answers is not None:
        # asks the user for confirmation
        if answers["final"]:
            print(
                "BE CAREFUL, after this operation the product will be no longer modifiable"
            )
        confirm_question = [
            inquirer.Confirm(
                "confirm",
                message=f"Add transformation, with carbon footprint of {answers['CF']}, to the product?",
            )
        ]
        confirm = inquirer.prompt(confirm_question, theme=load_theme_from_dict(theme))
        # if the user confirms the transaction is started.
        if confirm is not None and confirm["confirm"]:
            success = transformer.add_transformation_on_blockchain(
                int(answers["CF"]), answers["product_id"], answers["final"]
            )
            if success:
                print("Operation completed successfully")


def transfer_product(web3: Web3):
    """This function lets the transformer user transfer the property
    of a product to another transformer

    Args:
        web3 (Web3): used to access the address of the current user
    """
    try:
        transformer = Transformer(web3)
    except requests_exceptions.ConnectionError:
        print("Could not connect to the blockchain. Try again")
        return
    # get products associated with user address
    user_products = transformer.get_updatable_user_products(web3.eth.default_account)

    if len(user_products) == 0:
        print("You don't have any product to transfer\n")
        return

    print(
        "Follow the instructions to complete transfer process."
        "You can cancel operation in any moment by pressing Ctrl+C"
    )
    product_choice = [
        inquirer.List(
            "product_id",
            message="What product do you want to transfer?",
            choices=[
                (str(product.product_id) + " - " + product.name, product.product_id)
                for product in user_products
            ],
            carousel=True,
        )
    ]
    transformer_choice = [
        inquirer.Text(
            "transformer",
            message="Insert recipient's address",
            validate=validation.address_validation,
        )
    ]
    answers_product = inquirer.prompt(product_choice, theme=load_theme_from_dict(theme))
    if answers_product is not None:
        answers_transformer = inquirer.prompt(
            transformer_choice, theme=load_theme_from_dict(theme)
        )
        while (
            answers_transformer is not None
            and transformer.get_user_role(
                Web3.toChecksumAddress(answers_transformer["transformer"])
            )
            != 2
        ):
            print("Given address is not a transformer address. Please try again")
            answers_transformer = inquirer.prompt(
                transformer_choice, theme=load_theme_from_dict(theme)
            )
        # asks the user for confirmation
        if answers_transformer is not None:
            confirm_question = [
                inquirer.Confirm(
                    "confirm",
                    message=f"Transfer the selected product to the address {answers_transformer['transformer']}?",
                )
            ]
            confirm_answer = inquirer.prompt(
                confirm_question, theme=load_theme_from_dict(theme)
            )

            # if the user confirms the transaction is started.
            if confirm_answer is not None and confirm_answer["confirm"]:
                success = transformer.transfer_product_on_blockchain(
                    Web3.toChecksumAddress(answers_transformer["transformer"]),
                    answers_product["product_id"],
                )
                if success:
                    print("Operation completed successfully")


def create_new_product(web3: Web3):
    """This function lets the transformer create a new product,
    by selecting the necessary raw materials

    Args:
        web3 (Web3): used to access the address of the current user
    """
    try:
        transformer = Transformer(web3)
    except requests_exceptions.ConnectionError:
        print("Could not connect to the blockchain. Try again")
        return

    print(
        "Follow the instructions to create new product."
        "You can cancel operation in any moment by pressing Ctrl+C"
    )
    questions = [
        inquirer.Text(
            "name",  # asks the name of the product
            message="Type the name of the product you want to create",
            validate=validation.name_input_validation,
        ),
        inquirer.Checkbox(
            "raw_materials",  # The user selects the raw materials to use.
            message="Select a raw material to use (use space to select)",
            choices=[
                (material.__str__(), material.material_id)
                for material in transformer.get_usable_raw_materials(
                    web3.eth.default_account
                )
            ],
            validate=validation.raw_materials_selected,
        ),
    ]
    answers = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if answers is not None:
        # asks the user for confirmation
        confirm_question = [
            inquirer.Confirm(
                "confirm",
                message=f"Create the product \"{answers['name']}\" with selected materials?",
            )
        ]
        confirm_answer = inquirer.prompt(
            confirm_question, theme=load_theme_from_dict(theme)
        )
        # if the user confirms the transaction is started.
        if confirm_answer is not None and confirm_answer["confirm"]:
            success = transformer.create_new_product_on_blockchain(
                answers["name"], answers["raw_materials"]
            )
            if success:
                print("Operation completed successfully")
