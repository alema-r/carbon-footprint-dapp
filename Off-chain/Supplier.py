import inquirer


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

def raw_material_name_input_validation(answers, current):
    special_characters = "!@#$%^&*()-+?_=,<>\""
    if any(c in special_characters for c in current):
        raise inquirer.errors.ValidationError('', reason= 'Invalid input: Raw material\'s name can not contain special characters')    
    if len(current) == 0:
        raise inquirer.errors.ValidationError('', reason= 'Invalid input: Raw material\'s name can not be empty')    
    return True