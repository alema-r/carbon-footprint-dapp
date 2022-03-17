from cmath import nan
from xmlrpc.client import boolean
import inquirer
from web3 import Web3



def lot_input_validation(answers, current):
    try:
        int_cf=int(current)
    except:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Lot must be positive integer')
    if int_cf < 0:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Lot must be positive integer')
    return True

'''
Funzione che fa tutte le validazioni che richiedono un confronto fra materie prime e lotti.
'''
def input_validation(raw_material, raw_materials):
    # Controlla cha la materia prima e il lotto associato non siano già stati inseriti nei precedenti passaggi
    # Questo controllo funziona solo se tra materia prima e lotto c'è una corrispondenza uno a uno, che credo fosse il nostro caso
    # TODO: controllare anche con le materie prime che gia stanno sulla blockchain
    if raw_material in raw_materials:
        error_message = "Raw material and lot already inserted"
        return False, error_message
    
    return True, ''


def address_validation(contract,address, role = '') -> bool:
    '''
    Controlla se l'indirizzo inserito è valido.
    Prima controlla se l'indirizzo sia valido
    se viene specificato il ruolo controlla anche che l'indirizzo sia associato
    a quel particolare ruolo.
    Se tutto va bene ritorna true se non va bene riotrna Falso.
    '''
    try:
        checked_address = Web3.toChecksumAddress(address)
        real_role = contract.functions.getRole(checked_address)
    except Exception:
        return False
    if (role !=''):
        if (role == real_role):
            return True
        else:
            return False
    return True

'''
Funzione che controlla il corretto formato numerico della carbon footprint inserita dall'utente
'''
def carbon_fp_input_validation(answers, current):
    try:
        int_cf=int(current)
    except:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Carbon footprint must be positive integer')
    if int_cf < 0:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Carbon footprint must be positive integer')
    return True

def raw_material_name_input_validation(answers, current):
    special_characters = "!@#$%^&*()-+?_=,<>\""
    if any(c in special_characters for c in current):
        raise inquirer.errors.ValidationError('', reason= 'Invalid input: Product\'s name can not contain special characters')    
    if len(current) == 0:
        raise inquirer.errors.ValidationError('', reason= 'Invalid input: Product\'s name can not be empty')    
    return True
