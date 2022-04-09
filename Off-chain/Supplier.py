import inquirer
from BlockChain import create_raw_materials_on_blockchain
import validation
from Models import RawMaterial
from connection import web3
import re


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

    return True, ''



def insert_raw_material():
    """This function manages the interaction with a supplier in order to insert a new raw material on blockchain

    Args:
        contract (Contract): User Contract address used to call his functions 
        user_address (Address): Addres of the user (supplier) currently using the application 
    """
    raw_materials = []
    actions = ""

    # This while is used to manage the interaction with the supplier
    while (actions != "Done") & (actions != "Cancel"):
        # List of actions the user can perform
        actions = inquirer.list_input(
            message="Select \"Add new raw material\" to add new material or select \"Done\" to complete operation or select \"Cancel\" to cancel the operation",
            choices=["Add new raw material", "Done", "Cancel"]
        )
        # List of input the user should insert if he chooses to add new raw material
        if actions == "Add new raw material":
            questions = [
                inquirer.Text('raw material',
                              message="Insert new raw material name",
                              validate=validation.name_input_validation
                              ),
                inquirer.Text('lot',
                              message="Insert raw material's lot",
                              validate=validation.lot_input_validation
                              ),
                inquirer.Text('carbon footprint',
                              message="Insert raw material carbon footprint",
                              validate=validation.carbon_fp_input_validation
                              )
            ]
            # This line show all the questions coded above and the put the user's answers inside "answers" variable
            answers = inquirer.prompt(questions)
            # New raw material instance generated using user's inputs values
            raw_material_to_check = RawMaterial(answers["raw material"], int(answers['lot']), web3.default_account,
                                                int(answers['carbon footprint']))
            # The new raw material is validated. 
            valid, error_message = input_validation(raw_material_to_check, raw_materials)
            # If the new raw material is valid it is appended in the raw materials list 
            if valid:
                raw_materials.append(raw_material_to_check)
                print("New raw material correctly inserted")
                print(
                    "To add another raw material select \"Add new raw material\" or select \"Done\" to complete \
                    the operation")
            # If the added raw material is not valid an error message is shown to the user
            else:
                print(f"Invalid input: {error_message}")
                print('Select \"Add new raw material\" and try again or select \"Cancel\" to cancel the operation')

                # If the user chooses to Cancel the operation all inserted inputs are destroyed and the functions ends
    if actions == "Cancel":
        raw_materials = []
        return

    # When the user select Done, the interactions ends and the new added raw materials are insertend inside the blockchain
    if len(raw_materials) > 0:
        try:
            create_raw_materials_on_blockchain(raw_materials)
        # If the inserting operation fails, an error is printed. 
        except Exception as e:
            print(e)
            print("Please insert raw materials again")
