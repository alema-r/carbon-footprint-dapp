import inquirer


def raw_material_input_validation(answers, current):
    # controlla se la raw material inserita sia in caratteri alfanumerici
    if any(not c.isalnum() for c in current):
        raise inquirer.errors.ValidationError('', reason='Invalid format, insert valid formatted raw material. Use only alphanumeric character.')

    return True

def lot_input_validation(answers, current):
    if any(not c.isalnum() for c in current):
        raise inquirer.errors.ValidationError('', reason='Invalid format, insert valid formatted lot identifier. Use only alphanumeric character.')

    return True
'''
Funzione che fa tutte le validazioni che richiedono un confronto fra materie prime e lotti.
'''
def input_validation(raw_materials, lots, answers):
    # Controlla cha la materia prima e il lotto associato non siano già stati inseriti nei precedenti passaggi
    # Questo controllo funziona solo se tra materia prima e lotto c'è una corrispondenza uno a uno, che credo fosse il nostro caso
    # TODO: chiedere tra raw materia le lot c'è una corrispondenza uno a uno
    if not (answers['raw material'] & answers['lot']):
        error_message = "You must specify one raw material and one associated lot"
        return False, error_message

    if answers['raw material'] in raw_materials & answers['lot'] in lots:
        error_message = "Raw material and lot already inserted"
        return False, error_message
    
    return True, ''


def address_validation(answers, current):
    #TODO: do address validation and check
    return True

'''
Funzione che controlla il corretto formato numerico della carbon footprint inserita dall'utente
'''
def carbon_fp_input_validation(answers, current):
    try:
        int_cf=int(current['carbon footprint'])
    except:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Carbon footprint must be positive integer')
    if int_cf >= 0:
        return True
    else:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Carbon footprint must be positive integer')
        # Perchè non posso ritornare true?
        return True

