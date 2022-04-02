from random import choices
from Utils import carbon_fp_input_validation, address_validation
from BlockChain import connect
import inquirer
import Transformer
import Supplier
from Models import RawMaterial, Product
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

def add_transformation(user_products:list[Product], contract):
    '''This function lets the transformer user add a new trasformation to the production chain of a product that they own. 

    Keyword arguments:
    user_products -- the list of the products that the user currently owns
    contract -- the instance of Contract necessary to connect to the blockchain
    '''
    #ottengo i nomi dei prodotti dell'utente
    user_products_names = []
    for p in user_products:
        user_products_names.append(p.name)

    product_name = inquirer.list_input(
        message="What product do you want to update?",
        choices=user_products_names
    )

    #trovo l'id del prodotto con il nome selezionato
    for p in user_products:
        if p.name == product_name:
            product_id = p.productId
            break
    
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

def transfer_product(user_products:list[Product], contract):
    '''This function lets the transformer user transfer the property of a product to another transformer

    Keyword arguments
    user_products -- the list of the products that the user currently owns
    contract -- the instance of Contract necessary to connect to the blockchain
    '''
    #Ottengo i nomi dei prodotti dell'utente
    user_products_names = []
    for p in user_products:
        user_products_names.append(p.name)

    product_name = inquirer.list_input(
        message="What product do you want to transfer? ",
        choices=user_products_names
    )
    
    #Ottengo l'id del prodotto con il nome selezionato
    for p in user_products:
        if p.name == product_name:
            product_id = p.productId
            break

    address_ok = False
    while not address_ok:
        transfer_to = inquirer.text(
            message="Insert the address of the transformer to who you want to transfer the product: "
        )
        address_ok = address_validation(
            contract, transfer_to, "Transformer")
        if not address_ok:
            print("The specified address is not valid, please retry.")

    confirm = inquirer.confirm(
        message=f"Do you want to transfer the product {product_name} to the address {transfer_to}?"
    )
    if confirm:
        try:
            BlockChain.transfer_product_on_blockchain(
                contract, transfer_to, product_id)
        except Exception as e:
            print(e)
            print("Something went wrong while trying to trasfer the ownership of the product... Please retry.")

def create_new_product(contract):
    '''This function lets the transformer create a new product, by selecting the necessary raw materials
    
    Keyword arguments
    contract -- the instance of Contract necessary to connect to the blockchain'''
    raw_materials: list[RawMaterial] = BlockChain.get_raw_materials_from_blockchain(contract)

    product_name = inquirer.text(
        message="Type the name of the product you want to create: ",
        validate=Transformer.new_product_name_input_validation
    )
    
    #creo la lista delle scelte da mostrare all'utente e raccolgo gli indici delle materie prime usabili
    possible_choices=[]
    usable_materials_index=[]
    for index, material in enumerate(raw_materials):
        if not material.isUsed:
            possible_choices.append(f"Material name: {material.name}, lot: {material.lot}, supplier_address: {material.address}")
            usable_materials_index.append(index)
    
    #Faccio selezionare all'utente le materie prima da usare. Per ognuna di essere raccolgo l'id.
    add_new_material = True
    materials_to_use_indexes=[]
    while add_new_material:
        added_material = inquirer.list_input(
            message="Select a raw material to use",
            choices=possible_choices
        )
        #Gli elementi in possible_choices e usable_material_index hanno la stessa posizione nei rispettivi array se fanno riferimento
        #alla stessa materia prima.
        new_material_to_use_index = usable_materials_index[possible_choices.index(
            added_material)] 
        materials_to_use_indexes.append(new_material_to_use_index) #Qua prendo l'id
        possible_choices.remove(added_material) #Qua rimuovo la materia appena selezionata, così che non venga rimostrata
        usable_materials_index.remove(new_material_to_use_index) # Qua rimuovo l'id della materia appena selezionata
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

    # This while loop manages the initial interactions with the user
    while True:
        # Asks the user to declare his role and address
        questions = [
            inquirer.List('role',
                message="Specify your role",
                choices=["Client", "Supplier", "Transformer"],
            ),
            inquirer.Text('address',
                message = "Insert your address")
        ]
        # Prompt questions
        answers = inquirer.prompt(questions)
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
        all_products=BlockChain.get_products_from_blockchain(cf_contract)
        user_products = Transformer.get_updatable_user_products(
            all_products, user_contract.functions.CFaddress().call())
        action= inquirer.list_input(
            message="What action do you want to perform?",
            choices=role_dict[role]["actions"]
        )
        while action != "Exit":
            #SERVE UNA SORTA DI DO WHILE, COSI' NON CICLA
            if action == role_dict[role]["actions"][0]:
                get_filtered_products() #FUNZIONE COMUNE DA ISTANZIARE
            elif action == role_dict[role]["actions"][1]:
                create_new_product(cf_contract)
            elif action == role_dict[role]["actions"][2]:
                add_transformation(user_products, cf_contract)
            else:
                transfer_product(user_products, cf_contract)
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
                Supplier.insert_raw_material()
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
            cc = cf_contract.functions.getProducts().call()
            # chiamata al modulo che applica i filtri
        #if per il ruolo
            #if per l'operazione


if __name__ == "__main__":
    main()
