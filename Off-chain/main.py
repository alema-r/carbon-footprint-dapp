from connection import connect
import inquirer


role_dict = {
    "Client": {
        "num": "0",
        "actions": ["Search one or more products", "Exit"],
    },
    "Supplier": {
        "num": "1",
        "actions": [
            "Search one or more products",
            "Add a new product",
            "Transfer the property of a product",
            "Exit",
        ],
    },
    "Transformer": {
        "num": "2",
        "actions": [
            "Search one or more products",
            "Add a new operation",
            "Transfer the property of a product",
            "Exit",
        ],
    },
}

def main():

    print("Welcome!")

    role = inquirer.list_input(
        message="Specify your role",
        choices=["Client", "Supplier", "Transformer"],
    )

    print(role)
    contract = connect(role_dict[role]["num"])
    if role == "Transformer":
        pass
        #istanziazione transformer
    else:
        pass
        #istanziazione supplier

    action = inquirer.list_input(
        message="What action do you want to perform?",
        choices=role_dict[role]["actions"],
    )
    while action != "Exit":
        if action == role_dict[role]["actions"][0]:
            # scelta dei filtri
            cc = contract.functions.getProducts().call()
            # chiamata al modulo che applica i filtri
        #if per il ruolo
            #if per l'operazione

# logica supplier
# logica del transformer
# filtri
# anagrafica del prodotto


if __name__ == "__main__":
    main()
