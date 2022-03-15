import inquirer
import BlockChain
import Utils

def get_user_products(products, user_adress):
    '''This function filters the products stored in the blockhain. It returns a list of the products that are owned by the 
    current user.
    
    Keyword arguments:
    products -- the list of the products stored in the blockhain
    user_adress -- the adress of the current user
    '''
    user_products=[]
    for p in products:
        if p["currentOwner"]==user_adress: 
            user_products.append(p)
    return user_products

def add_transformation(user_products, contract):
    '''This function lets the transformer user add a new trasformation to the production chain of a product that they own. 

    Keyword arguments:
    user_products -- the list of the products that the user currently owns
    contract -- the instance of Contract necessary to connect to the blockchain
    '''
    user_products_names=[]
    for p in user_products:
        user_products_names.append(p["name"])

    product_name = inquirer.list_input(
        message="What product do you want to update?",
        choices=user_products_names
    )

    for p in user_products:
        if p["name"] == product_name:
            this_product=p
            break

    product_id = this_product["productId"]

    try:
        carb_foot=-1
        while carb_foot < 0 or not isinstance(carb_foot, int):
            carb_foot = int(inquirer.text(
                message="Insert the carbon footprint value of this transformation: ",
            ))
            if carb_foot < 0 or not isinstance(carb_foot, int) :
                print("The carbon footprint value needs to be an integer positive")
    except ValueError:
        print ("Please insert a valid carbon footprint value")
        carb_foot = int(inquirer.text(
            message="Insert the carbon footprint value of this transformation: ",
        ))

    ask_if_final = inquirer.list_input(
        message="Is this the final transformation?",
        choices=["No", "Yes"]
    )
    if ask_if_final == "Yes":
        is_the_final=True
    else:
        is_the_final = False

    confirm = inquirer.list_input(
        message="Do you want to add to the product "+product_name+"with a carbon footprint of "+carb_foot+" as the final\
             transformation for this product? " if is_the_final else "Do you want to add to the product "+product_name+"with a\
                  carbon footprint of "+carb_foot+"?",
        choices=["No", "Yes"]
    )
    if confirm=="Yes":
        try:
            BlockChain.add_transformation_on_blockchain(contract, carb_foot, product_id, is_the_final)
        except:
            print("Something went wrong while trying to add the trasnformation to the blockchain...")

    

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
    for p in user_products:
        if p["name"] == product_name:
            this_product = p
            break

    product_id = this_product["productId"]

    adress_ok=False
    while not adress_ok:
        transfer_to = inquirer.text(
            message="Insert the adress of the transformer to who you want to transfer the product: "
        )
        adress_ok = Utils.addres_validation(transfer_to)
        if not adress_ok:
            print("The specified adress is not valid, please retry.")

    confirm = inquirer.list_input(
        message="Do you want to transfer the product " +
        product_name + " to "+transfer_to+"?",
        choices=["No", "Yes"]
    )
    if confirm == "Yes":
        try:
            BlockChain.transfer_product_on_blockchain(contract, transfer_to, product_id)
        except:
            print("Something went wrong while trying to trasfer the ownership of the product...")
