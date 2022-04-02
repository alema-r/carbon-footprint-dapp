import inquirer
import contracts
from web3 import Web3
import Supplier
import Transformer

role_dict = {
    "Client": {
        "num": "0",
        "actions": {"Search one or more products": lambda a: a,  # get_filtered_products,
                    "Exit": exit
                    },
    },
    "Supplier": {
        "num": "1",
        "actions": {
            "Search one or more products": lambda a: a,
            "Add new raw materials": Supplier.insert_raw_material,
            "Exit": exit,
            },
    },
    "Transformer": {
        "num": "2",
        "actions": {
            "Search one or more products": lambda a: a,
            "Create a new product": Transformer.create_new_product,
            "Add a new operation": Transformer.add_transformation,
            "Transfer the property of a product": Transformer.transfer_product,
            "Exit": exit,
        },
    },
}

def address_validation(address, role = '') -> bool:
    '''
    Controlla se l'indirizzo inserito è valido.
    Prima controlla se l'indirizzo sia valido
    se viene specificato il ruolo controlla anche che l'indirizzo sia associato
    a quel particolare ruolo.
    Se tutto va bene ritorna true se non va bene riotrna Falso.
    '''
    try:
        checked_address = Web3.toChecksumAddress(address)
        real_role = contracts.user_contract.functions.getRole(checked_address)
    except Exception:
        return False
    if (role !=''):
        if (role == real_role):
            return True
        else:
            return False
    return True

def carbon_fp_input_validation(answers, current):
    """Functions that validates inserted carbon footprint value

    Args:
        answers (Dictionary): Dictinary of given answers
        current (Dictionary): Currenct given answer

    Raises:
        inquirer.errors.ValidationError: Raised if given carbon footprint isn't an integer
        inquirer.errors.ValidationError: Raised if given carbon footprint isn't positive

    Returns:
        Boolean: True if input is valid
    """
    try:
        int_cf=int(current)
    except:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Carbon footprint must be a positive integer')
    if int_cf <= 0:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Carbon footprint must be a positive integer')
    return True

