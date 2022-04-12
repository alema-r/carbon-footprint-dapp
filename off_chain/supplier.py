import inquirer
from inquirer.themes import load_theme_from_dict
from tabulate import tabulate

from . import blockchain
from . import connection
from .models import RawMaterial
from .theme_dict import theme
from . import validation


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
    """This function manages the interaction with a supplier in order to insert new raw materials on blockchain

    """
    raw_materials = []
    action = "start"
    # This while is used to manage the interaction with the supplier
    while (action != "Register raw materials") and (action != "Cancel insertion") and action is not None:
        # List of actions the user can perform
        if len(raw_materials) > 0:
            question = [inquirer.List(
                'action',
                message="Choose which action you want to perform",
                choices=["Add raw material", "Register raw materials", "Cancel insertion"]
            )]
        else:
            question = [inquirer.List(
                'action',
                message="Choose which action you want to perform",
                choices=["Add raw material", "Cancel insertion"]
            )]
        action = inquirer.prompt(question, theme=load_theme_from_dict(theme))
        # List of input the user should insert if he chooses to add new raw material
        if action is not None:
            if action['action'] == "Add raw material":
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
                answers = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
                # New raw material instance generated using user's inputs values
                if answers is not None:
                    raw_material_to_check = RawMaterial(answers["raw material"], int(answers['lot']), connection.web3.eth.default_account,
                                                        int(answers['carbon footprint']))
                    # The new raw material is validated.
                    valid, error_message = input_validation(raw_material_to_check, raw_materials)
                    # If the new raw material is valid it is appended in the raw materials list
                    if valid:
                        raw_materials.append(raw_material_to_check)
                        print("New raw material correctly inserted")
                    # If the added raw material is not valid an error message is shown to the user
                    else:
                        print(f"Invalid input: {error_message}")

            # If the user chooses to Cancel the operation all inserted inputs are destroyed and the functions ends
            elif action['action'] == "Cancel insertion":
                raw_materials = []
                return
            # When the user select Done, the interactions ends and the new added raw materials are insertend inside the blockchain
            else:
                # If the user wants to insert raw materials on blockchain
                if len(raw_materials) > 0:
                    # Tabulate is used to print raw materials in a fancy way
                    raw_materials_printable = []
                    for raw in raw_materials:
                        if len(raw.name) > 15:
                            name = raw.name[:15].rstrip() + "..."
                        else:
                            name = raw.name
                        
                        raw_materials_printable.append([name, raw.lot, raw.cf, raw.address])
                    table_raw_materials = tabulate(raw_materials_printable, headers=['Name', 'Lot', 'Carbon Footprint', 'Supplier'],
                                       tablefmt='tsv')
                    s = "Current inserted raw materials are:\n \n" + table_raw_materials +"\n"
                    print(s) 

                    # Asking the user for a confirm
                    question = [
                        inquirer.Confirm("confirm", message = "Do you want to insert listed raw materials? Press Y to confirm")
                    ]

                    answer = inquirer.prompt(question, theme = load_theme_from_dict(theme))

                    if answer is not None and answer['confirm']:
                        # if user confirm raw materials are added on blockchain
                        inserted = blockchain.create_raw_materials_on_blockchain(raw_materials)

                        if inserted:
                            # If raw materials are correctly added
                            print("Raw materials correctly inserted on Blockchain")

                        # If insertion fails or if it is succesfull list of raw materials are emptied anyway
                        raw_materials = []

                    elif answer is None:
                        raw_materials = []
                        # If the user doesn't confirm the insertion the while loop starts again
                        action = "start"
                    else:
                        action = "start"
