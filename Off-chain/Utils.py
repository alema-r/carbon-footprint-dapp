import inquirer
from web3 import Web3




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

