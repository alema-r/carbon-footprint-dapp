import inquirer
from BlockChain import connect
import connection
import Supplier
import Transformer
import Filter


def bye():
    print("Goodbye, have a nice day")
    exit(0)


role_dict = {
    "Client": {
        "num": "0",
        "actions": {"Search one or more products": Filter.filterProducts,
                    "Exit": bye
                    },
    },
    "Supplier": {
        "num": "1",
        "actions": {
            "Search one or more products": Filter.filterProducts,
            "Add new raw materials": Supplier.insert_raw_material,
            "Exit": bye,
        },
    },
    "Transformer": {
        "num": "2",
        "actions": {
            "Search one or more products": Filter.filterProducts,
            "Create a new product": Transformer.create_new_product,
            "Add a new operation": Transformer.add_transformation,
            "Transfer the property of a product": Transformer.transfer_product,
            "Exit": bye,
        },
    },
}


def main():
    while True:
        # Asks the user to declare his address
        questions = [
            inquirer.Text('address',
                          message="Insert your address")
        ]
        # Prompt questions
        answers = inquirer.prompt(questions)
        # Here it tries to connect to blockchain
        try:
            address = connect(connection.role, answers['address'])
            # if everything is ok the while loop ends
            break
        # if something goes wrong an exception is thrown
        except Exception as e:
            print(e)
            # The program asks the user to try again or to exit
            choice = inquirer.list_input(
                message="Select \"Try again\" to retry or \"Exit\" to close the application",
                choices=["Try again", "Exit"]
            )
            # if the user chooses to exit the program ends
            if choice == "Exit":
                return
    action = "start"
    if connection.role == int(role_dict['Transformer']['num']):
        while action != "Exit":
            action = inquirer.list_input(
                message="What action do you want to perform?",
                choices=role_dict['Transformer']["actions"]
            )
            if action in list(role_dict['Transformer']["actions"].keys())[2:4]:
                role_dict['Transformer']["actions"][action](address)
            else:
                role_dict['Transformer']["actions"][action]()
    elif connection.role == int(role_dict["Supplier"]['num']):
        # Inizia il meccanismo di interazione con l'utente.
        # Nel main si metterà solo la gestione dell'interazione con l'utente e l'interfaccia
        # TODO: finire la l'interazione con l'utente
        while action != "Exit":
            action = inquirer.list_input(
                message="What action do you want to perform?",
                choices=role_dict["Supplier"]["actions"]
            )
            if action == list(role_dict["Supplier"]["actions"].keys())[1]:
                role_dict["Supplier"]["actions"][action](address)
            else:
                role_dict["Supplier"]["actions"][action]()
    else:
        while action != "Exit":
            action = inquirer.list_input(
                message="What action do you want to perform?",
                choices=role_dict["Client"]["actions"],
            )
            role_dict["Client"]["actions"][action]()


if __name__ == "__main__":
    main()
