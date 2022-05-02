"""Module that implements a view for the supplier
"""
import inquirer
from inquirer.themes import load_theme_from_dict
from requests import exceptions as requests_exceptions
from tabulate import tabulate
from web3 import Web3

from off_chain.controller_supplier import Supplier
from off_chain.models import RawMaterial
from off_chain.theme_dict import theme
from off_chain import validation


def input_validation(raw_material, raw_materials):
    """Functions the checks if the user inserted two equals raw materials

    Args:
        raw_material (RawMaterial): last inserted raw material
        raw_materials (List[RawMaterial]): list of inserted raw materials

    Returns:
        Boolean: True if the input is valid else False
    """
    if raw_material in raw_materials:
        error_message = "Raw material and lot already inserted"
        return False, error_message

    return True, ""


def _new_raw_material_prompt(supplier: Supplier):
    """Manages the interaction with the user while inserting a new raw material

    Args:
        supplier (Supplier): instance of supplier controller

    Returns:
        dict, str: a dict of answers, an address of a transformer
    """
    questions = [
        inquirer.Text(
            "raw material",
            message="Insert new raw material name",
            validate=validation.name_input_validation,
        ),
        inquirer.Text(
            "lot",
            message="Insert raw material's lot",
            validate=validation.lot_input_validation,
        ),
        inquirer.Text(
            "carbon footprint",
            message="Insert raw material carbon footprint",
            validate=validation.carbon_fp_input_validation,
        ),
    ]
    transformer_choice = [
        inquirer.Text(
            "transformer",
            message="Insert recipient's address of raw material",
            validate=validation.address_validation,
        )
    ]
    # answers contains all the answers related to questions coded above
    answers = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if answers is not None:
        # The user inputs the address of the transformer. This then gets validated.
        answers_transformer = inquirer.prompt(
            transformer_choice, theme=load_theme_from_dict(theme)
        )
        while (
            answers_transformer is not None
            and supplier.get_user_role(
                Web3.toChecksumAddress(answers_transformer["transformer"])
            )
            != 2
        ):
            print("Given address is not a transformer address. Please try again")
            answers_transformer = inquirer.prompt(
                transformer_choice, theme=load_theme_from_dict(theme)
            )
        if answers_transformer is not None:
            return answers, answers_transformer["transformer"]
        return answers, None
    return None, None


def insert_raw_material(web3: Web3):
    """This function manages the interaction with a supplier
    in order to insert new raw materials on blockchain

    Args:
        web3 (Web3): instance of web3 connection to the blockchain
    """
    try:
        supplier = Supplier(web3)
    except requests_exceptions.ConnectionError:
        print("Could not connect to the blockchain. Try again")
        return
    raw_materials = []
    action = "start"
    # This while is used to manage the interaction with the supplier
    while (
        (action != "Register raw materials")
        and (action != "Cancel insertion")
        and action is not None
    ):
        # List of actions the user can perform
        if len(raw_materials) > 0:
            choices = [
                "Add raw material",
                "Register raw materials",
                "Cancel insertion",
            ]
        else:
            choices = [
                "Add raw material",
                "Cancel insertion",
            ]
        question = [
            inquirer.List(
                "action",
                message="Choose which action you want to perform",
                choices=choices,
            )
        ]
        action = inquirer.prompt(question, theme=load_theme_from_dict(theme))
        if action is not None:
            # List of inputs that the user should insert if they choose to add a new raw material
            if action["action"] == "Add raw material":
                answers, transformer_address = _new_raw_material_prompt(supplier)
                if answers is not None and transformer_address is not None:
                    # New raw material instance generated using user's inputs values
                    raw_material_to_check = RawMaterial(
                        answers["raw material"],
                        int(answers["lot"]),
                        web3.eth.default_account,
                        int(answers["carbon footprint"]),
                        transformer_address=Web3.toChecksumAddress(transformer_address),
                    )
                    # The new raw material is validated.
                    valid, error_message = input_validation(
                        raw_material_to_check, raw_materials
                    )
                    # If the new raw material is valid it is appended in the raw materials list
                    if valid:
                        raw_materials.append(raw_material_to_check)
                        print("New raw material is valid and ready to be inserted")
                    # If the added raw material is not valid an error message is shown to the user
                    else:
                        print(f"Invalid input: {error_message}")

            # If the user chooses to Cancel the operation all inserted inputs
            # are destroyed and the functions ends
            elif action["action"] == "Cancel insertion":
                raw_materials = []
                return
            # When the user select Done, the interactions ends and the new added raw materials
            # are inserted inside the blockchain
            else:
                # If the user wants to insert raw materials on blockchain
                if len(raw_materials) > 0:
                    # Tabulate is used to print raw materials in a fancy way
                    raw_materials_printable = []
                    for raw in raw_materials:
                        if len(raw.name) > 25:
                            name = raw.name[:22].rstrip() + "..."
                        else:
                            name = raw.name

                        raw_materials_printable.append(
                            [
                                name,
                                raw.lot,
                                raw.cf,
                                raw.address,
                                raw.transformer_address,
                            ]
                        )
                    table_raw_materials = tabulate(
                        raw_materials_printable,
                        headers=[
                            "Name",
                            "Lot",
                            "Carbon Footprint",
                            "Supplier",
                            "Transformer",
                        ],
                        tablefmt="tsv",
                    )
                    s = (
                        "Current inserted raw materials are:\n \n"
                        + table_raw_materials
                        + "\n"
                    )
                    print(s)

                    # Asking the user for a confirmation
                    question = [
                        inquirer.Confirm(
                            "confirm",
                            message="Insert listed raw materials? Press Y to confirm",
                        )
                    ]

                    answer = inquirer.prompt(
                        question, theme=load_theme_from_dict(theme)
                    )

                    if answer is not None and answer["confirm"]:
                        # if user confirm raw materials are added on blockchain
                        inserted = supplier.create_raw_materials_on_blockchain(
                            raw_materials
                        )

                        if inserted:
                            # If raw materials are correctly added
                            print("Raw materials correctly inserted on Blockchain")
                            return
                        # list of raw materials is emptied anyway
                        raw_materials = []

                    elif answer is None:
                        raw_materials = []
                        # If the user doesn't confirm the insertion the while loop starts again
                        action = "start"
                    else:
                        action = "start"
