from audioop import add
from operator import is_
from random import choices
from secrets import choice
from attr import validate
from idna import valid_contextj
from Utils import carbon_fp_input_validation, address_validation
from connection import connect
import inquirer
import Transformer
import Supplier
from Models import Raw_material
import BlockChain


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
            "Create a new product",
            "Add a new operation",
            "Transfer the property of a product",
            "Exit",
        ],
    },
}




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
            BlockChain.create_raw_materials_on_blockchain(contract, raw_materials)
        except Exception as e:
            print(e)
            print ("Please insert raw materials again")

def add_transformation(user_products, contract):
    '''This function lets the transformer user add a new trasformation to the production chain of a product that they own. 

    Keyword arguments:
    user_products -- the list of the products that the user currently owns
    contract -- the instance of Contract necessary to connect to the blockchain
    '''
    user_products_names = []
    for p in user_products:
        user_products_names.append(p["name"])

    product_name = inquirer.list_input(
        message="What product do you want to update?",
        choices=user_products_names
    )

    #SARA' DA CAMBIARE QUANDO SI FA LA CLASSE RELATIVA AL PRODOTTO, PER ORA JSON
    for p in user_products:
        if p["name"] == product_name:
            this_product = p
            break

    product_id = this_product["productId"]

    
    carb_footprint = inquirer.text(
        message="Insert the carbon footprint value of this transformation: ",
        validate = carbon_fp_input_validation
    )

    is_final = inquirer.confirm(
        message="Is this the final transformation?"
    )

    confirm = inquirer.confirm(
        message=f"Do you want to add to the product {product_name} with a carbon footprint of {carb_footprint} as the final\
             transformation for this product? " if is_final else f"Do you want to add to the product {product_name} with a\
                  carbon footprint of {carb_footprint}?"
    )
    if confirm:
        try:
            BlockChain.add_transformation_on_blockchain(
                contract, int(carb_footprint), product_id, is_final)
        except Exception as e:
            print(e)
            print("Something went wrong while trying to add the trasnformation to the blockchain... Please retry.")

def transfer_product(user_products, contract):
    '''This function lets the transformer user transfer the property of a product to another transformer

    Keyword arguments
    user_products -- the list of the products that the user currently owns
    contract -- the instance of Contract necessary to connect to the blockchain
    '''
    user_products_names = []
    for p in user_products:
        user_products_names.append(p["name"])

    product_name = inquirer.list_input(
        message="What product do you want to transfer? ",
        choices=user_products_names
    )
    #SARA' DA CAMBIARE QUANDO SI FA LA CLASSE RELATIVA AL PRODOTTO, PER ORA JSON
    for p in user_products:
        if p["name"] == product_name:
            this_product = p
            break

    product_id = this_product["productId"]

    adress_ok = False
    while not adress_ok:
        transfer_to = inquirer.text(
            message="Insert the adress of the transformer to who you want to transfer the product: "
        )
        adress_ok = address_validation(
            contract, transfer_to, "Transformer")
        if not adress_ok:
            print("The specified adress is not valid, please retry.")

    confirm = inquirer.confirm(
        message=f"Do you want to transfer the product {product_name} to {transfer_to}?"
    )
    if confirm:
        try:
            BlockChain.transfer_product_on_blockchain(
                contract, transfer_to, product_id)
        except Exception as e:
            print(e)
            print("Something went wrong while trying to trasfer the ownership of the product... Please retry.")

def create_new_product(contract):
    raw_materials = BlockChain.get_raw_materials_from_blockchain(contract)

    product_name = inquirer.text(
        message="Type the name of the product you want to create: ",
        validate=Transformer.new_product_name_input_validation
    )
    
    possible_choices=[]
    usable_materials_index=[]
    for index, material in raw_materials:
        if not material.get_isUsed():
            possible_choices.append(f"Material name: {material.get_name()}, lot: {material.get_lot()}, supplier_address: {material.get_address}")
            usable_materials_index.append(index)
    
    add_new_material = True
    materials_to_use_indexes=[]
    while add_new_material:
        added_material = inquirer.list_input(
            message="Select a raw material to use",
            choices=possible_choices
        )
        new_material_to_use_index = usable_materials_index[possible_choices.index(
            added_material)]
        materials_to_use_indexes.append(new_material_to_use_index)
        possible_choices.remove(added_material)
        usable_materials_index.remove(new_material_to_use_index)

        add_more = inquirer.confirm(
            message="Do you want to add another raw material?"
        )
        add_new_material = add_more
    
    confirm = inquirer.confirm(
        message=f'Do you want to create the product "{product_name} with the selected materials?' #pescare i nomi è un casino...
    )
    if confirm:
        try:
            BlockChain.create_new_product_on_blockchain(
                contract, product_name, materials_to_use_indexes)
        except Exception as e:
            print(e)
            print("Please insert the new product again...")

def main():

    print("Welcome!")

    role = inquirer.list_input(
        message="Specify your role",
        choices=["Client", "Supplier", "Transformer"],
    )

    print(role)
    contract, user_adress = connect(role_dict[role]["num"])
    #QUANDO PRENDIAMO I PRODOTTI?
    action = "start"
    if role == "Transformer":
        userProducts=Transformer.get_updatable_user_products(products, user_adress)
        action= inquirer.list_input(
            message="What action do you want to perform?",
            choices=role_dict[role]["actions"]
        )
        while action != "Exit":
            #SERVE UNA SORTA DI DO WHILE, COSI' NON CICLA
            if action == role_dict[role]["actions"][0]:
                get_filtered_products() #FUNZIONE COMUNE DA ISTANZIARE
            elif action == role_dict[role]["actions"][1]:
                create_new_product(contract)
            elif action == role_dict[role]["actions"][2]:
                add_transformation(userProducts, contract)
            else:
                transfer_product(userProducts, contract)
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


if __name__ == "__main__":
    main()
