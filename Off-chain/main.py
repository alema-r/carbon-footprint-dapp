from BlockChain import connect
import inquirer
from contracts import cf_contract
from Utils import role_dict


def main():
    print("Welcome!")
    # This while loop manages the initial interactions with the user
    while True:
        # Asks the user to declare his role and address
        questions = [
            inquirer.List('role',
                          message="Specify your role",
                          choices=["Client", "Supplier", "Transformer"],
                          ),
            inquirer.Text('address',
                          message="Insert your address")
        ]
        # Prompt questions
        answers = inquirer.prompt(questions)
        address = answers['address']
        # Here it tries to connect to blockchain
        try:
            web3 = connect(role_dict[answers['role']]["num"], answers['address'])
            role = answers['role']
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
    if role == "Transformer":
        while action != "Exit":
            action = inquirer.list_input(
                message="What action do you want to perform?",
                choices=role_dict[role]["actions"]
            )
            if action in role_dict[role]["actions"].keys()[:2]:
                role_dict[role]["actions"][action]()
            else:
                role_dict[role]["actions"][action](address)

            '''
            if action == role_dict[role]["actions"][0]:
                get_filtered_products()  # FUNZIONE COMUNE DA ISTANZIARE
            elif action == role_dict[role]["actions"][1]:
                Transformer.create_new_product()
            elif action == role_dict[role]["actions"][2]:
                Transformer.add_transformation(user_products)
            else:
                Transformer.transfer_product(user_products)
            '''
        # istanziazione transformer
    elif role == "Supplier":
        # Inizia il meccanismo di interazione con l'utente.
        # Nel main si metterà solo la gestione dell'interazione con l'utente e l'interfaccia
        # TODO: finire la l'interazione con l'utente
        while action != "Exit":
            action = inquirer.list_input(
                message="What action do you want to perform?",
                choices=role_dict[role]["actions"]
            )
            role_dict[role]["actions"][action]()
    else:
        while action != "Exit":
            action = inquirer.list_input(
                message="What action do you want to perform?",
                choices=role_dict[role]["actions"],
            )
            role_dict[role]["actions"][action]()

    while action != "Exit":
        if action == role_dict[role]["actions"][0]:
            # scelta dei filtri
            cc = cf_contract.functions.getProducts().call()
            # chiamata al modulo che applica i filtri
        # if per il ruolo
        # if per l'operazione


if __name__ == "__main__":
    main()
