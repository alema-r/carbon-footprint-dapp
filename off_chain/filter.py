import operator
from tabulate import tabulate
import inquirer
from inquirer.themes import load_theme_from_dict
from web3 import Web3

from off_chain import base_controller
from off_chain.base_controller import BlockChain
from off_chain.theme_dict import theme
from off_chain import validation


def personalized_contains(a: str, b: str):
    return a.lower() in b.lower()


def simple_filter(result: list, criteria: dict) -> list:
    """This function applies a filter on the products list.

        Args:
            result (List): list of product id where the function appends valid results
            criteria (Dictionary):
                Dictionary containing the function used to get products data, the name of the field, the value and the
                operator to use in the filtering process and a boolean indicating if data is being gathered from
                blockchain events

        Returns:
            'list[int]': list containing all the identifiers that are in result or which product satisfies the filter
    """
    elements = criteria["elements"]()
    if criteria["event"]:
        for e in elements:
            if criteria["operator"](e["args"][criteria["field"]], criteria["value"]) and e['args']['pId'] not in result:
                result.append(e["args"]["pId"])
    else:
        for e in elements:
            if criteria["operator"](getattr(e, criteria["field"]), criteria["value"]):
                result.append(e.product_id)
    return result


def or_filter(result, criteria):
    """This function implements the OR logic for multiple filter.

    Args:
        result (List): list of product id obtained from a previous filter
        criteria (Dictionary):
            Dictionary containing the function used to get products data, the name of the field, the value and the
            operator to use in the filtering process and a boolean indicating if data is being gathered from
            blockchain events

    Returns:
        'list[int]': list containing all the identifiers that either are in results or which product satisfies
            the filter
    """
    simple_filter(result, criteria)
    return list(set(result))


def and_filter(result, criteria):
    """This function implements the AND logic for multiple filter.

    Args:
        result (List): list of product id obtained from a previous filter
        criteria (Dictionary):
            Dictionary containing the function used to get products data, the name of the field, the value and the
            operator to use in the filtering process and a boolean indicating if data is being gathered from
            blockchain events

    Returns:
        'list[int]': list containing all the identifiers that are in results and which product satisfies
            the filter
    """
    temp = simple_filter([], criteria)
    temp2 = result.copy()
    for e in temp2:
        if e not in temp:
            result.remove(e)
    return result


def print_products(block_chain: BlockChain, ids):
    """This function prints a table containing products basic information.

    Args:
        block_chain (BlockChain): instance of base controller to interact with blockchain
        ids (List): list of identifiers of the products to print
    """
    products_printable = []
    for pid in ids:
        p = block_chain.get_product(pid)
        products_printable.append([p.product_id, p.name, p.address, p.cf, p.is_ended])
    table = tabulate(products_printable, headers=["Id", "Name", "Owner", "CF", "isEnded"], tablefmt="tsv")
    print(table)


def detailed_print(block_chain: BlockChain, pid):
    """This function prints all the details regarding one product.

    Args:
        block_chain (BlockChain): instance of base controller to interact with blockchain
        pid: ID of the product
    """
    product = block_chain.get_product_details(pid)
    print(product.__str__())


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
        ("Lower equal", operator.le)
    ]
    questions = [inquirer.List(
        'op',
        message="Select an operator",
        choices=choices
    )]
    choice = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if choice is not None:
        return choice['op']
    else:
        return None


def filter_products(web3: Web3, results=None, filters=simple_filter):
    """This functions manages the filtering process

    Args:
        web3 (Web3): instance of web3 connection to the blockchain
        results (List): list of productId that are currently the result of the filtering process
        filters (Callable): filter function to call
    """
    block_chain = base_controller.BlockChain(web3)
    if results is None:
        results = []
    criteria = {}
    choices = ["Name", "Owner", "CF", "Ended", "Supplier", "Transformer", "Raw Material"]
    print("Follow the instructions to search products and view details. You can cancel any operation at any moment "
          "by pressing Ctrl+C")
    question = [inquirer.List(
        "field",
        message="Select a field",
        choices=choices
    )]
    action = inquirer.prompt(question, theme=load_theme_from_dict(theme))
    if action is not None:
        if action['field'] == choices[0]:  # NAME
            questions = [inquirer.Text(
                "name",
                message="Name",
                validate=validation.name_input_validation
            )]
            value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if value is not None:
                criteria = {"elements": block_chain.get_all_products, "value": value['name'].lower(), "field": "name",
                            "operator": personalized_contains, "event": False}
        elif action['field'] == choices[1]:  # OWNER
            questions = [inquirer.Text(
                "Owner",
                message="Owner's address",
                validate=validation.address_validation
            )]
            value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            while value is not None and block_chain.get_user_role(Web3.toChecksumAddress(value['Owner'])) != 2:
                print("Given address is not a transformer address. Please try again")
                value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if value is not None:
                criteria = {"elements": block_chain.get_all_products, "value": Web3.toChecksumAddress(value['Owner']),
                            "field": "address", "operator": operator.eq, "event": False}
        elif action['field'] == choices[2]:  # CF
            op = select_operator()
            if op is not None:
                questions = [inquirer.Text(
                    'CF',
                    message="CF value",
                    validate=validation.carbon_fp_input_validation
                )]
                value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
                if value is not None:
                    criteria = {"elements": block_chain.get_all_products, "value": int(value['CF']), "field": "cf",
                                "operator": op, "event": False}
        elif action['field'] == choices[3]:  # IS ENDED
            choices = [("Yes", True), ("No", False)]
            questions = [inquirer.List(
                'isEnded',
                message="Is it ended?",
                choices=choices
            )]
            value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if value is not None:
                criteria = {"elements": block_chain.get_all_products, "value": value['isEnded'], "field": "is_ended",
                            "operator": operator.eq, "event": False}
        elif action['field'] == choices[4]:  # SUPPLIERS
            questions = [inquirer.Text(
                'Supplier',
                message="Supplier's address",
                validate=validation.address_validation
            )]
            value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            while value is not None and block_chain.get_user_role(Web3.toChecksumAddress(value['Supplier'])) != 1:
                print("Given address is not a supplier address. Please try again")
                value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if value is not None:
                criteria = {"elements": block_chain.event_logs.get_raw_materials_used_events,
                            "value": Web3.toChecksumAddress(value['Supplier']), "field": "supplier",
                            "operator": operator.eq, "event": True}
        elif action['field'] == choices[5]:  # TRANSFORMERS
            questions = [inquirer.Text(
                'Transformer',
                message="Transformer's address",
                validate=validation.address_validation
            )]
            value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            while value is not None and block_chain.get_user_role(Web3.toChecksumAddress(value['Transformer'])) != 2:
                print("Given address is not a transformer address. Please try again")
                value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if value is not None:
                criteria = {"elements": block_chain.event_logs.get_transformations_events,
                            "value": Web3.toChecksumAddress(value['Transformer']), "field": "userAddress",
                            "operator": operator.eq, "event": True}
        elif action['field'] == choices[6]:  # RAW MATERIAL NAME
            questions = [inquirer.Text(
                'RawMaterial',
                message="Raw Material name",
                validate=validation.name_input_validation
            )]
            value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if value is not None:
                criteria = {"elements": block_chain.event_logs.get_raw_materials_used_events,
                            "value": value['RawMaterial'], "field": "name", "operator": personalized_contains,
                            "event": True}
        if criteria:
            results = filters(results, criteria)
        if len(results) > 0:
            choices = ["Print search results", "Add another filter(AND logic)", "Add another filter(OR logic)",
                       "Exit"]
            question = [inquirer.List(
                'action',
                message="Which action do you want to perform?",
                choices=choices
            )]
            action = inquirer.prompt(question, theme=load_theme_from_dict(theme))
            if action is not None:
                if action['action'] == choices[0]:
                    print_products(block_chain, results)
                    question = [inquirer.Text(
                        'PID',
                        message="Insert a product ID to see product details",
                        validate=validation.id_input_validation
                    )]
                    value = inquirer.prompt(question, theme=load_theme_from_dict(theme))
                    if value is not None:
                        detailed_print(block_chain, int(value['PID']))
                elif action['action'] == choices[1]:
                    filter_products(web3, results, and_filter)
                elif action['action'] == choices[2]:
                    filter_products(web3, results, or_filter)
        elif criteria:
            print("\nNo products match the specified filter\n")
