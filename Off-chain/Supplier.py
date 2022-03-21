import inquirer


def lot_input_validation(answers, current):
    """Functions that validates lot

    Args:
        answers (Dictionary): Dictionary of given answers
        current (Dictionary): Current given answer

    Raises:
        inquirer.errors.ValidationError: Raised if the lot's value isn't an integer
        inquirer.errors.ValidationError: Raised if lot's value isn't positive

    Returns:
        Boolean: True if the input is valid
    """
    try:
        int_cf=int(current)
    except:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Lot must be positive integer')
    if int_cf < 0:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: Lot must be positive integer')
    return True

def input_validation(raw_material, raw_materials):
    """Functions the checks if the user inserted two equals raw materials

    Args:
        raw_material (RawMaterial): last inserted raw material
        raw_materials (List[RawMaterial]): list of inserted raw materials

    Returns:
        Boolean: True if the input is valid else False
    """
    if raw_material in raw_materials:
        error_message = "Raw material and lot already inserted"
        return False, error_message
    
    return True, ''

def raw_material_name_input_validation(answers, current):
    """Functions that validates raw material's name inserted by user

    Args:
        answers (Dictionary): Dictionary of inserted answers
        current (Dictionary): Current given answer

    Raises:
        inquirer.errors.ValidationError: Raised if raw material's name contains special characters
        inquirer.errors.ValidationError: Raised if raw material's name is an empty string

    Returns:
        Boolean: True if the input is valid
    """
    special_characters = "!@#$%^&*()-+?_=,<>\""
    if any(c in special_characters for c in current):
        raise inquirer.errors.ValidationError('', reason= 'Invalid input: Raw material\'s name can not contain special characters')    
    if len(current) == 0:
        raise inquirer.errors.ValidationError('', reason= 'Invalid input: Raw material\'s name can not be empty')    
    return True