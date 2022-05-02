"""Module used to filter the product search
"""
import operator
from typing import Union

from tabulate import tabulate
import inquirer
from inquirer.themes import load_theme_from_dict
from requests import exceptions as requests_exceptions
from web3 import Web3

from off_chain.base_controller import BlockChain
from off_chain.theme_dict import theme
from off_chain import validation


def personalized_contains(container: str, contained: str) -> bool:
    """Checks if a string is contained in another string

    Args:
        container (str): the longest string
        contained (str): the shortest string

    Returns:
        bool: True if contained is within container
    """
    return contained.lower() in container.lower()


def simple_filter(result: list, criteria: dict) -> list:
    """This function applies a filter on the products list.

    Args:
        result (List): list of product id where the function appends valid results
        criteria (Dictionary):
            Dictionary containing the function used to get products data,
            the name of the field, the value and the operator to use in the
            filtering process and a boolean indicating if data is being
            gathered from blockchain events

    Returns:
        'list[int]': list containing all the identifiers that are in result
            or which product satisfies the filter
    """
    elements = criteria["elements"]()
    if criteria["event"]:
        for elem in elements:
            if (
                criteria["operator"](elem["args"][criteria["field"]], criteria["value"])
                and elem["args"]["pId"] not in result
            ):
                result.append(elem["args"]["pId"])
    else:
        for elem in elements:
            if criteria["operator"](
                getattr(elem, criteria["field"]), criteria["value"]
            ):
                result.append(elem.product_id)
    return result


def or_filter(result, criteria):
    """This function implements the OR logic for multiple filter.

    Args:
        result (List): list of product id obtained from a previous filter
        criteria (Dictionary):
            Dictionary containing the function used to get products data,
            the name of the field, the value and the operator to use in the
            filtering process and a boolean indicating if data is being
            gathered from blockchain events

    Returns:
        'list[int]': list containing all the identifiers that either are in results
            or which product satisfies the filter
    """
    simple_filter(result, criteria)
    return list(set(result))


def and_filter(result, criteria):
    """This function implements the AND logic for multiple filter.

    Args:
        result (List): list of product id obtained from a previous filter
        criteria (Dictionary):
            Dictionary containing the function used to get products data,
            the name of the field, the value and the operator to use in the
            filtering process and a boolean indicating if data is being
            gathered from blockchain events

    Returns:
        'list[int]': list containing all the identifiers that are in results and
            which product satisfies the filter
    """
    temp = simple_filter([], criteria)
    temp2 = result.copy()
    for elem in temp2:
        if elem not in temp:
            result.remove(elem)
    return result


def print_products(block_chain: BlockChain, ids):
    """This function prints a table containing products basic information.

    Args:
        block_chain (BlockChain): instance of base controller to interact with blockchain
        ids (List): list of identifiers of the products to print
    """
    products_printable = []
    for pid in ids:
        prod = block_chain.get_product(pid)
        products_printable.append(
            [prod.product_id, prod.name, prod.address, prod.cf, prod.is_ended]
        )
    table = tabulate(
        products_printable,
        headers=["Id", "Name", "Owner", "CF", "isEnded"],
        tablefmt="tsv",
    )
    print(table)


def detailed_print(block_chain: BlockChain, pid):
    """This function prints all the details regarding one product.

    Args:
        block_chain (BlockChain): instance of base controller to interact with blockchain
        pid: ID of the product
    """
    product = block_chain.get_product_details(pid)
    if product is not None:
        print(product)


def select_operator():
    """This function makes the user select an operator from a given list

    Returns:
        'operator': the operator selected by the user
    """
    choices = [
        ("Equal", operator.eq),
        ("Greater", operator.gt),
        ("Greater equal", operator.ge),
        ("Lower", operator.lt),
        ("Lower equal", operator.le),
    ]
    questions = [inquirer.List("op", message="Select an operator", choices=choices)]
    choice = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if choice is not None:
        return choice["op"]
    return None


def _product_name_choice(block_chain: BlockChain) -> Union[dict, None]:
    """Manages the choice of the product name during the filtering process

    Args:
        block_chain (BlockChain): instance of base controller to interact with blockchain

    Returns:
        Union[dict, None]: the dict of criterias or None
    """
    questions = [
        inquirer.Text("name", message="Name", validate=validation.name_input_validation)
    ]
    value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if value is not None:
        criteria = {
            "elements": block_chain.get_all_products,
            "value": value["name"],
            "field": "name",
            "operator": personalized_contains,
            "event": False,
        }
        return criteria
    return None


def _owner_choice(block_chain: BlockChain) -> Union[dict, None]:
    """Manages the choice of the owner during the filtering process

    Args:
        block_chain (BlockChain): instance of base controller to interact with blockchain

    Returns:
        Union[dict, None]: the dict of criterias or None
    """
    questions = [
        inquirer.Text(
            "Owner",
            message="Owner's address",
            validate=validation.address_validation,
        )
    ]
    value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    while (
        value is not None
        and block_chain.get_user_role(Web3.toChecksumAddress(value["Owner"])) != 2
    ):
        print("Given address is not a transformer address. Please try again")
        value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if value is not None:
        criteria = {
            "elements": block_chain.get_all_products,
            "value": Web3.toChecksumAddress(value["Owner"]),
            "field": "address",
            "operator": operator.eq,
            "event": False,
        }
        return criteria
    return None


def _cf_choice(block_chain: BlockChain) -> Union[dict, None]:
    """Manages the choice of the cf value during the filtering process

    Args:
        block_chain (BlockChain): instance of base controller to interact with blockchain

    Returns:
        Union[dict, None]: the dict of criterias or None
    """
    op = select_operator()
    if op is not None:
        questions = [
            inquirer.Text(
                "CF",
                message="CF value",
                validate=validation.carbon_fp_input_validation,
            )
        ]
        value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
        if value is not None:
            criteria = {
                "elements": block_chain.get_all_products,
                "value": int(value["CF"]),
                "field": "cf",
                "operator": op,
                "event": False,
            }
            return criteria
    return None


def _is_ended_choice(block_chain: BlockChain) -> Union[dict, None]:
    """Manages the choice of the finished status of a product during the filtering process

    Args:
        block_chain (BlockChain): instance of base controller to interact with blockchain

    Returns:
        Union[dict, None]: the dict of criterias or None
    """
    choices = [("Yes", True), ("No", False)]
    questions = [inquirer.List("isEnded", message="Is it ended?", choices=choices)]
    value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if value is not None:
        criteria = {
            "elements": block_chain.get_all_products,
            "value": value["isEnded"],
            "field": "is_ended",
            "operator": operator.eq,
            "event": False,
        }
        return criteria
    return None


def _supplier_choice(block_chain: BlockChain) -> Union[dict, None]:
    """Manages the choice of the supplier during the filtering process

    Args:
        block_chain (BlockChain): instance of base controller to interact with blockchain

    Returns:
        Union[dict, None]: the dict of criterias or None
    """
    questions = [
        inquirer.Text(
            "Supplier",
            message="Supplier's address",
            validate=validation.address_validation,
        )
    ]
    value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    while (
        value is not None
        and block_chain.get_user_role(Web3.toChecksumAddress(value["Supplier"])) != 1
    ):
        print("Given address is not a supplier address. Please try again")
        value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if value is not None:
        criteria = {
            "elements": block_chain.event_logs.get_raw_materials_used_events,
            "value": Web3.toChecksumAddress(value["Supplier"]),
            "field": "supplier",
            "operator": operator.eq,
            "event": True,
        }
        return criteria
    return None


def _transformer_choice(block_chain: BlockChain) -> Union[dict, None]:
    """Manages the choice of the transformer during the filtering process

    Args:
        block_chain (BlockChain): instance of base controller to interact with blockchain

    Returns:
        Union[dict, None]: the dict of criterias or None
    """
    questions = [
        inquirer.Text(
            "Transformer",
            message="Transformer's address",
            validate=validation.address_validation,
        )
    ]
    value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    while (
        value is not None
        and block_chain.get_user_role(Web3.toChecksumAddress(value["Transformer"])) != 2
    ):
        print("Given address is not a transformer address. Please try again")
        value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if value is not None:
        criteria = {
            "elements": block_chain.event_logs.get_transformations_events,
            "value": Web3.toChecksumAddress(value["Transformer"]),
            "field": "userAddress",
            "operator": operator.eq,
            "event": True,
        }
        return criteria
    return None


def _raw_material_choice(block_chain: BlockChain) -> Union[dict, None]:
    """Manages the choice of the raw material name during the filtering process

    Args:
        block_chain (BlockChain): instance of base controller to interact with blockchain

    Returns:
        Union[dict, None]: the dict of criterias or None
    """
    questions = [
        inquirer.Text(
            "RawMaterial",
            message="Raw Material name",
            validate=validation.name_input_validation,
        )
    ]
    value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if value is not None:
        criteria = {
            "elements": block_chain.event_logs.get_raw_materials_used_events,
            "value": value["RawMaterial"],
            "field": "name",
            "operator": personalized_contains,
            "event": True,
        }
        return criteria
    return None


def filter_products(web3: Web3, results=None, filters=simple_filter):
    """This functions manages the filtering process

    Args:
        web3 (Web3): instance of web3 connection to the blockchain
        results (List): list of productId that are currently the result of the filtering process
        filters (Callable): filter function to call
    """
    try:
        block_chain = BlockChain(web3)
    except requests_exceptions.ConnectionError:
        print("Could not connect to the blockchain. Try again")
        return

    if results is None:
        results = []
    criteria = {}
    choices = [
        ("Name", _product_name_choice),
        ("Owner", _owner_choice),
        ("CF", _cf_choice),
        ("Ended", _is_ended_choice),
        ("Supplier", _supplier_choice),
        ("Transformer", _transformer_choice),
        ("Raw Material", _raw_material_choice),
    ]
    print(
        "Follow the instructions to search products and view details."
        "You can cancel any operation at any moment by pressing Ctrl+C"
    )
    question = [inquirer.List("field", message="Select a field", choices=choices)]
    action = inquirer.prompt(question, theme=load_theme_from_dict(theme))
    if action is not None:
        criteria = action["field"](block_chain)

        if criteria:
            results = filters(results, criteria)

        if len(results) > 0:
            choices = [
                "Print search results",
                "Add another filter(AND logic)",
                "Add another filter(OR logic)",
                "Exit",
            ]
            question = [
                inquirer.List(
                    "action",
                    message="Which action do you want to perform?",
                    choices=choices,
                )
            ]
            action = inquirer.prompt(question, theme=load_theme_from_dict(theme))
            if action is not None:
                if action["action"] == choices[0]:
                    print_products(block_chain, results)
                    question = [
                        inquirer.Text(
                            "PID",
                            message="Insert a product ID to see product details",
                            validate=validation.id_input_validation,
                        )
                    ]
                    value = inquirer.prompt(question, theme=load_theme_from_dict(theme))
                    if value is not None:
                        detailed_print(block_chain, int(value["PID"]))
                elif action["action"] == choices[1]:
                    filter_products(web3, results, and_filter)
                elif action["action"] == choices[2]:
                    filter_products(web3, results, or_filter)
        elif criteria:
            print("\nNo products match the specified filter\n")
