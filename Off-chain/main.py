from Utils import carbon_fp_input_validation
from connection import connect
import inquirer
import Transformer
import Supplier
from Models import Raw_material
from BlockChain import create_raw_materials_on_blockchain


role_dict = {
    "Client": {
        "num": "0",
        "actions": ["Search one or more products", "Exit"],
    },
    "Supplier": {
        "num": "1",
        "actions": [
            "Search one or more products",
            "Add new raw materials",
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
    contract, user_adress = connect(role_dict[role]["num"])
    #I PRODOTTI ANDREBBERO PRESTI TUTTI SUBITO, SERVONO A TUTTI
    action = "start"
    if role == "Transformer":
        userProducts=Transformer.get_user_products(products, user_adress)
        action= inquirer.list_input(
            message="What action do you want to perform?",
            choices=role_dict[role]["actions"]
        )
        while action != "Exit":
            #SERVE UNA SORTA DI DO WHILE, COSI' NON CICLA
            if action == role_dict[role]["actions"][0]:
                get_filtered_products() #FUNZIONE COMUNE DA ISTANZIARE
            elif action == role_dict[role]["actions"][1]:
                Transformer.add_transformation(userProducts, contract)
            else:
                Transformer.transfer_product(userProducts, contract)
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
                insert_raw_material(contract, user_adress)
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



def insert_raw_material(contract, user_address):
    raw_materials = []
    actions = ""

    while (actions != "Done") & (actions != "Cancel"):
        actions = inquirer.list_input(
            message= "Select \"Add new raw material\" to add new material or select \"Done\" to complete operation or select \"Cancel\" to cancel the operation",
            choices=["Add new raw material", "Done", "Cancel"]
        )
        if actions == "Add new raw material":
            questions = [
            inquirer.Text('raw material',
            message="Insert new raw material name",
            validate=Supplier.raw_material_name_input_validation
            ),
            inquirer.Text('lot',
            message="Insert raw material's lot",
            validate=Supplier.lot_input_validation
            ),
            inquirer.Text('carbon footprint',
            message = "Insert raw material carbon footprint",
            validate=carbon_fp_input_validation
            )
            ]
            # Il propt salva le risposte in un dizionario dove la chiave è la domanda e il valore è la risposta dell'utente
            answers = inquirer.prompt(questions)
            raw_material_to_check = Raw_material(answers["raw material"], int(answers['lot']), user_address, int(answers['carbon footprint']))
            # Una volta ricevute le risposte esse vanno validate e sanificate.
            valid, error_message = Supplier.input_validation(raw_material_to_check, raw_materials) 
            if valid:
                raw_materials.append(raw_material_to_check)
                print("New raw material correctly inserted")
                print("To add another raw material select \"Add new raw material\" or select \"Done\" to complete the operation")
            else:
                print(f"Invalid input: {error_message}")
                print('Select \"Add new raw material\" and try again or select \"Cancel\" to cancel the operation') 
    
    # Se l'operazione viene annullata la funzione termina
    if actions == "Cancel":
        raw_materials = []
        return
    
    # Una volta finito l'inserimento delle materie prime per il prodotto e per il lotto si può chiamare la funzione per inserire
    # il nuovo prodotto sulla blockchain
    if (len(raw_materials) > 0):
        try:
            create_raw_materials_on_blockchain(contract, raw_materials)
        except Exception as e:
            print(e)
            print ("Per favore inserire di nuovo le materie prime")


if __name__ == "__main__":
    main()
