import inquirer
from typing import Tuple
import re
from web3 import Web3
import BlockChain


def supplier_address_validation(answers, current) -> Tuple[bool, any]:
    """Function that validates an address

    Args:
        answers (Dictionary): All given answers
        current (Dictionary): Current given answers.

    Returns:
        Bool: Returns True if addres is valide else returns false
    """
    try:
        role = BlockChain.get_user_role(current)
    except:
        raise inquirer.errors.ValidationError('', reason="Invalid supplier address. Please try again")

    if Web3.isAddress(current) and 1 == role:
        return True
    else:
        raise inquirer.errors.ValidationError('', reason="Invalid supplier address. Please try again")


def transformer_address_validation(answers, current) -> Tuple[bool, any]:
    """Function that validates an address

    Args:
        answers (Dictionary): All given answers
        current (Dictionary): Current given answers.

    Returns:
        Bool: Returns True if address is valid else returns False
    """
    try:
        role = BlockChain.get_user_role(current)
    except:
        raise inquirer.errors.ValidationError('', reason="Invalid transformer address. Please try again")

    if Web3.isAddress(current) and 1 == role:
        return True
    else:
        raise inquirer.errors.ValidationError('', reason="Invalid transformer address. Please try again")


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
        int_cf = int(current)
    except:
        raise inquirer.errors.ValidationError('', reason='Invalid input: Carbon footprint must be a positive integer')
    if int_cf <= 0:
        raise inquirer.errors.ValidationError('', reason='Invalid input: Carbon footprint must be a positive integer')
    return True


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
        int_lot = int(current)
    except:
        raise inquirer.errors.ValidationError('', reason='Invalid input: Lot must be positive integer or 0')
    if int_lot < 0:
        raise inquirer.errors.ValidationError('', reason='Invalid input: Lot must be positive integer or 0')
    return True


def id_input_validation(answers, current):
    """Functions that validates product's id
    Args:
        answers (Dictionary): Dictionary of given answers
        current (Dictionary): Current given answer
    Raises:
        inquirer.errors.ValidationError: Raised if the id's value isn't an integer
        inquirer.errors.ValidationError: Raised if id's value isn't greater than 0
    Returns:
        Boolean: True if the input is valid
    """
    if current != '':
        try:
            int_id = int(current)
        except Exception:
            raise inquirer.errors.ValidationError('', reason='Invalid input: ID must be an integer greater than 0')
        if int_id < 0:
            raise inquirer.errors.ValidationError('', reason='Invalid input: ID must be an integer greater than 0')
        return True
    return True


def name_input_validation(answers, current):
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
    pattern = "^[a-zA-Z0-9 ]{2,}$"
    if bool(re.match(pattern, current.strip(' '))):
        return True
    else:
        raise inquirer.errors.ValidationError('', reason=f'Invalid input: Inserted name is invalid. Please \
        insert names with only letters and numbers or type almost one character')