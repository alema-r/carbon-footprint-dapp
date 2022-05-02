"""Module that contains input validation used in inquirer questions
"""
import re

import inquirer
from web3 import Web3
from web3.constants import ADDRESS_ZERO


def address_validation(answers, current):
    """Function that validates an address

    Args:
        answers (Dictionary): All given answers
        current (Dictionary): Current given answers.

    Returns:
        Bool: Returns True if address is valid else returns false
    """
    try:
        address = Web3.toChecksumAddress(current.strip(" "))
        if address == ADDRESS_ZERO:
            raise Exception
    except Exception:
        raise inquirer.errors.ValidationError(
            "", reason="Invalid address format. Please try again"
        )
    return True


def carbon_fp_input_validation(answers, current):
    """Functions that validates inserted carbon footprint value

    Args:
        answers (Dictionary): Dictionary of given answers
        current (Dictionary): Current given answer

    Raises:
        inquirer.errors.ValidationError: Raised if given carbon footprint isn't an integer
        inquirer.errors.ValidationError: Raised if given carbon footprint isn't positive

    Returns:
        Boolean: True if input is valid
    """
    current_to_test = current.strip(" ")
    try:
        int_cf = int(current_to_test)
    except Exception:
        raise inquirer.errors.ValidationError(
            "", reason="Invalid input: Carbon footprint must be a positive integer"
        )
    if int_cf <= 0 or int_cf > 1000000:
        raise inquirer.errors.ValidationError(
            "",
            reason="Invalid input: Carbon footprint must be a positive integer with a max value of 1000000",
        )
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
    current_to_test = current.strip(" ")
    try:
        int_lot = int(current_to_test)
    except Exception:
        raise inquirer.errors.ValidationError(
            "", reason="Invalid input: Lot must be positive integer or 0"
        )
    if int_lot < 0 or int_lot > 1000000:
        raise inquirer.errors.ValidationError(
            "",
            reason="Invalid input: Lot must be positive integer or 0 with a max value of 1000000",
        )
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
    current_to_test = current.strip(" ")
    try:
        int_id = int(current_to_test)
    except Exception:
        raise inquirer.errors.ValidationError(
            "", reason="Invalid input: ID must be an integer greater than 0"
        )
    if int_id < 0:
        raise inquirer.errors.ValidationError(
            "", reason="Invalid input: ID must be an integer greater than 0"
        )
    return True


def name_input_validation(answers, current):
    """Functions that validates the raw material's or product's name inserted by user

    Args:
        answers (Dictionary): Dictionary of inserted answers
        current (Dictionary): Current given answer

    Raises:
        inquirer.errors.ValidationError: Raised if the raw material's/product's name contains specials characters
        inquirer.errors.ValidationError: Raised if the raw material's/product's name is an empty string

    Returns:
        Boolean: True if the input is valid
    """
    pattern = "^[a-zA-Z0-9 ]{2,50}$"
    if bool(re.match(pattern, current.strip(" "))):
        return True
    else:
        raise inquirer.errors.ValidationError(
            "",
            reason=f"Invalid input: Inserted name is invalid. Please insert names with only letters and numbers with at least one and at most fifty characters",
        )


def raw_materials_selected(answers, current):
    if len(current) > 0:
        return True
    else:
        raise inquirer.errors.ValidationError(
            "", reason="You must select at least one raw material"
        )
