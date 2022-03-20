import inquirer
from Models import Product

def get_updatable_user_products(products:list[Product], user_address):
    '''This function filters the products stored in the blockhain. It returns a list of the products that are owned by the 
    current user.
    
    Keyword arguments:
    products -- the list of the products stored in the blockhain
    user_adress -- the adress of the current user
    '''
    user_products=[]
    for p in products:
        if p.address==user_address and not p.isEnded: 
            user_products.append(p)
    return user_products


def new_product_name_input_validation(answers, current):
    special_characters = "!@#$%^&*()-+?_=,<>\""
    if any(c in special_characters for c in current):
        raise inquirer.errors.ValidationError(
            '', reason='Invalid input: product\'s name can not contain special characters')
    if len(current) == 0:
        raise inquirer.errors.ValidationError(
            '', reason='Invalid input: product\'s name can not be empty')
    return True