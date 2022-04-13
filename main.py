import sys

import inquirer
from inquirer.themes import load_theme_from_dict

from off_chain.theme_dict import theme
from off_chain import blockchain, connection, filter, supplier, transformer, contracts, event_logs


def bye():
    print("Goodbye, have a nice day")
    exit(0)


role_dict = {
    "Client": {
        "num": "0",
        "actions": [("Search one or more products", filter.filter_products),
                    ("Exit", bye)
        ],
    },
    "Supplier": {
        "num": "1",
        "actions": [
            ("Search one or more products", filter.filter_products),
            ("Add new raw materials", supplier.insert_raw_material),
            ("Exit", bye),
        ],
    },
    "Transformer": {
        "num": "2",
        "actions": [
            ("Search one or more products", filter.filter_products),
            ("Create a new product", transformer.create_new_product),
            ("Add a new operation", transformer.add_transformation),
            ("Transfer the property of a product", transformer.transfer_product),
            ("Exit", bye),
        ],
    },
}


def main():
    print("Welcome!")
    questions = [
        inquirer.List('role',
                      message="Specify your role",
                      choices=[("Client", 0), ("Supplier", 1), ("Transformer", 2), ("Exit", -1)],
                      )
    ]

    answers = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if answers is not None and answers['role'] != -1:
        # getting user role to instantiate connection to the correct node
        role = answers['role']
        connection.connection(role)
        contracts.building_contracts()
        event_logs.building_filters()

    else:
        print("Goodbye have a nice day")
        exit(0)
    while True:
        # Asks the user to declare his address
        questions = [
            inquirer.Text('address',
                          message="Insert your address") # aggiungere validazione dell'indirizzo
        ]
        # Prompt questions
        answers = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
        # Here it tries to connect to blockchain
        try:
            address = blockchain.set_account_as_default(role, answers['address'])
            # if everything is ok the while loop ends
            break
        # if something goes wrong an exception is thrown
        except Exception as e:
            print(e)
            # The program asks the user to try again or to exit
            questions = [inquirer.List(
                'retry',
                message="Select \"Try again\" to retry or \"Exit\" to close the application",
                choices=["Try again", "Exit"]
            )]
            choice = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            # if the user chooses to exit the program ends
            if choice['retry'] == "Exit":
                bye()

    action = "start"
    # If the chosen role is Transformer
    if role == int(role_dict['Transformer']['num']):
        while action != "Exit":
            questions = [inquirer.List(
                "action",
                message="What action do you want to perform?",
                choices=role_dict['Transformer']["actions"],
            )]
            action = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if action is not None:
                if action["action"] == transformer.add_transformation or action['action'] == transformer.transfer_product:
                    action["action"](address)
                else:
                    action["action"]()

    # If the chosen role is Supplier
    elif role == int(role_dict["Supplier"]['num']):
        # Inizia il meccanismo di interazione con l'utente.
        # Nel main si metterà solo la gestione dell'interazione con l'utente e l'interfaccia
        while action != "Exit":
            questions = [inquirer.List(
                "action",
                message="What action do you want to perform?",
                choices=role_dict["Supplier"]["actions"],
            )]
            action = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if action is not None:
                action["action"]()

    # If the chosen role is Client
    else:
        while action != "Exit":
            questions = [inquirer.List(
                "action",
                message="What action do you want to perform?",
                choices=role_dict["Client"]["actions"],
            )]
            action = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if action is not None:
                action["action"]()


if __name__ == "__main__":
    main()
