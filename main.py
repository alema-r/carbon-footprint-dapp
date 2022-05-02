"""Entrypoint of the application
"""
import sys

import inquirer
from inquirer.themes import load_theme_from_dict

from off_chain.theme_dict import theme
from off_chain import (
    base_controller,
    connection,
    filters,
    view_supplier,
    view_transformer,
)


def bye():
    """Prints an exit message exit and stops the application"""
    print("Goodbye, have a nice day")
    sys.exit(0)


role_dict = {
    "Client": {
        "num": "0",
        "actions": [
            ("Search one or more products", filters.filter_products),
            ("Exit", bye),
        ],
    },
    "Supplier": {
        "num": "1",
        "actions": [
            ("Search one or more products", filters.filter_products),
            ("Add new raw materials", view_supplier.insert_raw_material),
            ("Exit", bye),
        ],
    },
    "Transformer": {
        "num": "2",
        "actions": [
            ("Search one or more products", filters.filter_products),
            ("Create a new product", view_transformer.create_new_product),
            ("Add a new operation", view_transformer.add_transformation),
            ("Transfer the property of a product", view_transformer.transfer_product),
            ("Exit", bye),
        ],
    },
}


def main():
    print("Welcome!")
    questions = [
        inquirer.List(
            "role",
            message="Specify your role",
            choices=[
                ("Client", int(role_dict["Client"]["num"])),
                ("Supplier", int(role_dict["Supplier"]["num"])),
                ("Transformer", int(role_dict["Transformer"]["num"])),
                ("Exit", -1),
            ],
        )
    ]

    answers = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if answers is not None and answers["role"] != -1:
        # getting user role to instantiate connection to the correct node
        role = answers["role"]
        web3 = connection.connection(role)
        if not web3.isConnected():
            print("Could not connect to the blockchain, Try again")
            sys.exit(1)
        block_chain = base_controller.BlockChain(web3)

    else:
        bye()

    while True:
        # Asks the user to declare his address
        questions = [inquirer.Text("address", message="Insert your address")]
        # Prompt questions
        answers = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
        if answers is not None:
            # Here it tries to connect to blockchain
            try:
                block_chain.set_account_as_default(role, answers["address"])
                # if everything is ok the while loop ends
                break
            # if something goes wrong an exception is thrown
            except Exception as error:
                print(error)
                # The program asks the user to try again or to exit
                questions = [
                    inquirer.List(
                        "retry",
                        message='Select "Try again" to retry or "Exit" to close the application',
                        choices=["Try again", "Exit"],
                    )
                ]
                choice = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
                # if the user chooses to exit the program ends
                if choice["retry"] == "Exit":
                    bye()
        else:
            bye()

    # If the chosen role is Transformer
    if role == int(role_dict["Transformer"]["num"]):
        while True:
            questions = [
                inquirer.List(
                    "action",
                    message="What action do you want to perform?",
                    choices=role_dict["Transformer"]["actions"],
                )
            ]
            action = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if action is not None:
                if action["action"] != bye:
                    action["action"](web3)
                else:
                    action["action"]()

    # If the chosen role is Supplier
    elif role == int(role_dict["Supplier"]["num"]):
        while True:
            questions = [
                inquirer.List(
                    "action",
                    message="What action do you want to perform?",
                    choices=role_dict["Supplier"]["actions"],
                )
            ]
            action = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if action is not None:
                if action["action"] != bye:
                    action["action"](web3)
                else:
                    action["action"]()

    # If the chosen role is Client
    else:
        while True:
            questions = [
                inquirer.List(
                    "action",
                    message="What action do you want to perform?",
                    choices=role_dict["Client"]["actions"],
                )
            ]
            action = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if action is not None:
                if action["action"] != bye:
                    action["action"](web3)
                else:
                    action["action"]()


if __name__ == "__main__":
    main()
