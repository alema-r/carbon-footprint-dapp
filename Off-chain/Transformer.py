import inquirer
from numpy import add_newdoc
from Models import Product
from BlockChain import add_transformation_on_blockchain, transfer_product_on_blockchain, create_new_product_on_blockchain, get_raw_material_not_used
from Utils import carbon_fp_input_validation, address_validation
from Models import RawMaterial


def get_updatable_user_products(products: list[Product], user_address):
    '''This function filters the products stored in the blockhain. It returns a list of the products that are owned by the 
    current user.

    Keyword arguments:
    products -- the list of the products stored in the blockhain
    user_adress -- the adress of the current user
    '''
    """
    user_products=[]
    for p in products:
        if p.address==user_address and not p.isEnded: 
            user_products.append(p)
    """
    return list(filter(lambda p: (p.address == user_address and not p.isEnded), products))


def new_product_name_input_validation(answers, current):
    special_characters = "!@#$%^&*()-+?_=,<>\""
    if any(c in special_characters for c in current):
        raise inquirer.errors.ValidationError(
            '', reason='Invalid input: product\'s name can not contain special characters')
    if len(current) == 0:
        raise inquirer.errors.ValidationError(
            '', reason='Invalid input: product\'s name can not be empty')
    return True


def add_transformation(user_products: list[Product]):
    '''This function lets the transformer user add a new trasformation to the production chain of a product that they own. 

    Keyword arguments:
    user_products -- the list of the products that the user currently owns
    contract -- the instance of Contract necessary to connect to the blockchain
    '''
    # ottengo i nomi dei prodotti dell'utente
    user_products_names = []
    for p in user_products:
        user_products_names.append(p.name)

    product_name = inquirer.list_input(
        message="What product do you want to update?",
        choices=user_products_names
    )

    # trovo l'id del prodotto con il nome selezionato
    for p in user_products:
        if p.name == product_name:
            product_id = p.productId
            break

    carb_footprint = inquirer.text(
        message="Insert the carbon footprint value of this transformation: ",
        validate=carbon_fp_input_validation
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
            add_transformation_on_blockchain(
                int(carb_footprint), product_id, is_final)
        except Exception as e:
            print(e)
            print(
                "Something went wrong while trying to add the trasnformation to the blockchain... Please retry.")


def transfer_product(user_products: list[Product]):
    '''This function lets the transformer user transfer the property of a product to another transformer

    Keyword arguments
    user_products -- the list of the products that the user currently owns
    contract -- the instance of Contract necessary to connect to the blockchain
    '''
    # Ottengo i nomi dei prodotti dell'utente
    user_products_names = []
    for p in user_products:
        user_products_names.append(p.name)

    product_name = inquirer.list_input(
        message="What product do you want to transfer? ",
        choices=user_products_names
    )

    # Ottengo l'id del prodotto con il nome selezionato
    for p in user_products:
        if p.name == product_name:
            product_id = p.productId
            break

    address_ok = False
    while not address_ok:
        transfer_to = inquirer.text(
            message="Insert the address of the transformer to who you want to transfer the product: "
        )
        address_ok = address_validation(transfer_to, "Transformer")
        if not address_ok:
            print("The specified address is not valid, please retry.")

    confirm = inquirer.confirm(
        message=f"Do you want to transfer the product {product_name} to the address {transfer_to}?"
    )
    if confirm:
        try:
            transfer_product_on_blockchain(transfer_to, product_id)
        except Exception as e:
            print(e)
            print(
                "Something went wrong while trying to trasfer the ownership of the product... Please retry.")


def create_new_prodcut():
    """This function lets the transformer create a new product, by selecting the necessary raw materials"""

    product_name = inquirer.text(
        message="Type the name of the product you want to create: ",
        validate=new_product_name_input_validation
    )
    raw_materials = get_raw_material_not_used()
    
    # creo la lista delle scelte da mostrare all'utente
    possible_choices = []
    for material in raw_materials:
        possible_choices.append(
            f"Material name: {material.name}, lot: {material.lot}, supplier_address: {material.address}")

    # Faccio selezionare all'utente le materie prima da usare. Per ognuna di essere raccolgo l'id.
    add_new_material = True
    materials_to_use_ids = []
    while add_new_material:
        added_material = inquirer.list_input(
            message="Select a raw material to use",
            choices=possible_choices
        )
        # Gli elementi in possible_choices e raw_materials
        # hanno la stessa posizione nei rispettivi array se fanno riferimento
        # alla stessa materia prima.
        position = possible_choices.index(added_material)
        materials_to_use_ids.append(raw_materials[position].materialId)
        # Qua rimuovo la materia appena selezionata, così che non venga rimostrata
        possible_choices.remove(added_material)
        raw_materials.remove(raw_materials[position])
        add_more = inquirer.confirm(
            message="Do you want to add another raw material?"
        )
        add_new_material = add_more

    confirm = inquirer.confirm(
        message=f'Do you want to create the product "{product_name} with the selected materials?'
    )
    if confirm:
        try:
            create_new_product_on_blockchain(
                product_name, materials_to_use_ids)
        except Exception as e:
            print(e)
            print("Please insert the new product again...")


'''
def create_new_product():
    """This function lets the transformer create a new product, by selecting the necessary raw materials
    
    Keyword arguments
    contract -- the instance of Contract necessary to connect to the blockchain"""
    raw_materials: list[RawMaterial] = get_all_raw_materials()

    product_name = inquirer.text(
        message="Type the name of the product you want to create: ",
        validate=new_product_name_input_validation
    )

    #creo la lista delle scelte da mostrare all'utente e raccolgo gli indici delle materie prime usabili
    possible_choices = []
    usable_materials_index = []
    for index, material in enumerate(raw_materials):
        if not material.isUsed:
            possible_choices.append(
                f"Material name: {material.name}, lot: {material.lot}, supplier_address: {material.address}")
            usable_materials_index.append(index)

    #Faccio selezionare all'utente le materie prima da usare. Per ognuna di essere raccolgo l'id.
    add_new_material = True
    materials_to_use_indexes = []
    while add_new_material:
        added_material = inquirer.list_input(
            message="Select a raw material to use",
            choices=possible_choices
        )
        #Gli elementi in possible_choices e usable_material_index hanno la stessa posizione nei rispettivi array se fanno riferimento
        #alla stessa materia prima.
        new_material_to_use_index = usable_materials_index[possible_choices.index(
            added_material)]
        materials_to_use_indexes.append(
            new_material_to_use_index)  # Qua prendo l'id
        # Qua rimuovo la materia appena selezionata, così che non venga rimostrata
        possible_choices.remove(added_material)
        # Qua rimuovo l'id della materia appena selezionata
        usable_materials_index.remove(new_material_to_use_index)
        add_more = inquirer.confirm(
            message="Do you want to add another raw material?"
        )
        add_new_material = add_more

    confirm = inquirer.confirm(
        # pescare i nomi è un casino...
        message=f'Do you want to create the product "{product_name} with the selected materials?'
    )
    if confirm:
        try:
            create_new_product_on_blockchain(product_name, materials_to_use_indexes)
        except Exception as e:
            print(e)
            print("Please insert the new product again...")
'''
