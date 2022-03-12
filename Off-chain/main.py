from email import message
from connection import connect
import inquirer
import Transformer
import Supplier


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
    contract, userAdress = connect(role_dict[role]["num"])
    #I PRODOTTI ANDREBBERO PRESTI TUTTI SUBITO, SERVONO A TUTTI
    action = "start"
    if role == "Transformer":
        userProducts=Transformer.getUserProducts(products, userAdress)
        action= inquirer.list_input(
            message="What action do you want to perform?",
            choices=role_dict[role]["actions"]
        )
        while action != "Exit":
            #SERVE UNA SORTA DI DO WHILE, COSI' NON CICLA
            if action == role_dict[role]["actions"][0]:
                get_filtere_products() #FUNZIONE COMUNE DA ISTANZIARE
            elif action == role_dict[role]["actions"][1]:
                Transformer.addTransformation(userProducts, contract)
            else:
                Transformer.transferProduct(userProducts, contract)
        #istanziazione transformer
    elif role == "Supplier":
        # Inizia il meccanismo di interazione con l'utente. 
        # Nel main si metterà solo la gestione dell'interazione con l'utente e l'interfaccia
        # TODO: finire la l'interazione con l'utente
        while action != "Exit":
            action = inquirer.list_input(
                message="What action do you want to perform?",
                choices=role_dict[role]["actions"]
            )
            if action == role_dict[role]["actions"][0]:
                get_filtered_products()
            if action == role_dict[role]["actions"][1]:
                Supplier.create_product()
            if action == role_dict[role]["actions"][2]:
                Supplier.transfer_product()
    else :
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
