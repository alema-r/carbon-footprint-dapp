from Utils import carbon_fp_input_validation, address_validation
from connection import connect
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

def insert_raw_material(contract, user_address):
    """This function manages the interaction with a supplier in order to insert a new raw material on blockchain

    Args:
        contract (Contract): User Contract address used to call his functions 
        user_address (Address): Addres of the user (supplier) currently using the application 
    """
    raw_materials = []
    actions = ""

    # This while is used to manage the interaction with the supplier
    while (actions != "Done") & (actions != "Cancel"):
        # List of actions the user can perform
        actions = inquirer.list_input(
            message= "Select \"Add new raw material\" to add new material or select \"Done\" to complete operation or select \"Cancel\" to cancel the operation",
            choices=["Add new raw material", "Done", "Cancel"]
        )
        # List of input the user should insert if he chooses to add new raw material
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
            # This line show all the questions coded above and the put the user's answers inside "answers" variable
            answers = inquirer.prompt(questions)
            # New raw material instance generated using user's inputs values
            raw_material_to_check = RawMaterial(answers["raw material"], int(answers['lot']), user_address, int(answers['carbon footprint']))
            # The new raw material is validated. 
            valid, error_message = Supplier.input_validation(raw_material_to_check, raw_materials) 
            # If the new raw material is valid it is appended in the raw materials list 
            if valid:
                raw_materials.append(raw_material_to_check)
                print("New raw material correctly inserted")
                print("To add another raw material select \"Add new raw material\" or select \"Done\" to complete the operation")
            # If the added raw material is not valid an error message is shown to the user
            else:
                print(f"Invalid input: {error_message}")
                print('Select \"Add new raw material\" and try again or select \"Cancel\" to cancel the operation') 
    
    # If the user chooses to Cancel the operation all inserted inputs are destroyed and the functions ends
    if actions == "Cancel":
        raw_materials = []
        return
    
    # When the user select Done, the interactions ends and the new added raw materials are insertend inside the blockchain
    if (len(raw_materials) > 0):
        try:
            BlockChain.create_raw_materials_on_blockchain(contract, raw_materials)
        # If the inserting operation fails, an error is printed. 
        except Exception as e:
            print(e)
            print ("Please insert raw materials again")

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
    """This function lets the transformer create a new product, by selecting the necessary raw materials
    
    Keyword arguments
    contract -- the instance of Contract necessary to connect to the blockchain"""
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

    role = inquirer.list_input(
        message="Specify your role",
        choices=["Client", "Supplier", "Transformer"],
    )

    print(role)
    #contract, user_adress = connect(role_dict[role]["num"])
    web3, user_contract, cf_contract = connect(role_dict[role]["num"])
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
                insert_raw_material(
                    cf_contract, user_contract.functions.CFaddress().call())
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
