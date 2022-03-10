import inquirer
from web3 import Web3

def getUserProducts(products, userAdress):
    userProducts=[]
    for p in products:
        if p["currentOwner"]==userAdress: 
            userProducts.append(p)
    return userProducts

def addTransformation(userProducts, contract):
    userProductsNames=[]
    for p in userProducts:
        userProductsNames.append(p["name"])

    productName = inquirer.list_input(
        message="What product do you want to update?",
        choices=userProductsNames
    )

    for p in userProducts:
        if p["name"]==productName:
            thisProduct=p
            break

    productId=thisProduct["productId"]

    carbFoot = int(inquirer.text(
        message="Insert the carbon footprint value of this transformation: ",
    ))

    askIfFinal = inquirer.list_input(
        message="Is this the final transformation?",
        choices=["No", "Yes"]
    )
    if askIfFinal == "Yes":
        isTheFinal=True
    else:
        isTheFinal=False

    confirm = inquirer.list_input(
        message="Do you want to add to the product "+productName+"with a carbon footprint of "+carbFoot+" as the final transformation\
             for this product? " if isTheFinal else "Do you want to add to the product "+productName+"with a\
                  carbon footprint of "+carbFoot+"?",
        choices=["No", "Yes"]
    )
    if confirm=="Yes":
        contract.functions.addTransformation(carbFoot, productId, isTheFinal).transact()

    

def transferProduct(userProducts, contract):
    userProductsNames = []
    for p in userProducts:
        userProductsNames.append(p["name"])
    productName = inquirer.list_input(
        message="What product do you want to transfer? ",
        choices=userProductsNames
    )
    for p in userProducts:
        if p["name"] == productName:
            thisProduct = p
            break

    productId = thisProduct["productId"]

    transferTo = inquirer.text(
        message="Insert the adress of the transformer to who you want to transfer the product: "
    )
    #CONTROLLO DELL'INDIRIZZO?
    confirm = inquirer.list_input(
        message="Do you want to transfer the product "+productName+ " to "+transferTo+"?",
        choices=["No", "Yes"]
    )
    if confirm == "Yes":
        contract.functions.transferCP(transferTo,productId).transact()
