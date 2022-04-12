import operator
from tabulate import tabulate
import inquirer
from inquirer.themes import load_theme_from_dict
from theme_dict import theme
import BlockChain
import event_logs
from web3 import Web3
import validation


def personalized_contains(a: str, b: str):
    return a.lower().__contains__(b.lower())


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


def print_products(ids):
    """This function prints a table containing products basic information.

    Args:
        ids (List): list of identifiers of the products to print
    """
    products_printable = []
    for pid in ids:
        p = BlockChain.get_product(pid)
        products_printable.append([p.product_id, p.name, p.address, p.cf, p.is_ended])
    table = tabulate(products_printable, headers=["Id", "Name", "Owner", "CF", "isEnded"], tablefmt="tsv")
    print(table)


def detailed_print(id):
    """This function prints all the details regarding one product.

    Args:
        id: Id of the product
    """
    product = BlockChain.get_product_details(id)
    print(product.__str__())


def select_operator():
    """This function makes the user select an operator from a given list

    Returns:
        'operator': the operator selected by the user
    """
    choices = ["Equal", "Greater", "Greater equal", "Lower", "Lower equal"]
    questions = [inquirer.List(
        'op',
        message="Select an operator",
        choices=choices
    )]
    action = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
    if action is not None:
        if action['op'] == choices[0]:
            op = operator.eq
        elif action['op'] == choices[1]:
            op = operator.gt
        elif action['op'] == choices[2]:
            op = operator.ge
        elif action['op'] == choices[3]:
            op = operator.lt
        elif action['op'] == choices[4]:
            op = operator.le
        return op
    else:
        return None


def filter_products(results=None, filters=simple_filter):
    """This functions manages the filtering process

    Args:
        results (List): list of productId that are currently the result of the filtering process
        filters (Callable): filter function to call
    """
    if results is None:
        results = []
    criteria = {}
    choices = ["Name", "Owner", "CF", "Ended", "Supplier", "Transformer",
               "Raw Material"]
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
                criteria = {"elements": BlockChain.get_all_products, "value": value['name'].lower(), "field": "name",
                            "operator": personalized_contains, "event": False}
        elif action['field'] == choices[1]:  # OWNER
            questions = [inquirer.Text(
                "Owner",
                message="Owner's address",
                validate=validation.transformer_address_validation
            )]
            value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if value is not None:
                criteria = {"elements": BlockChain.get_all_products, "value": Web3.toChecksumAddress(value['Owner']),
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
                    criteria = {"elements": BlockChain.get_all_products, "value": int(value['CF']), "field": "cf",
                                "operator": op, "event": False}
        elif action['field'] == choices[3]:  # ISENDED
            choices = [("Yes", True), ("No", False)]
            questions = [inquirer.List(
                'isEnded',
                message="Is it ended?",
                choices=choices
            )]
            value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if value is not None:
                criteria = {"elements": BlockChain.get_all_products, "value": value['isEnded'], "field": "is_ended",
                            "operator": operator.eq, "event": False}
        elif action['field'] == choices[4]:  # SUPPLIERS
            questions = [inquirer.Text(
                'Supplier',
                message="Supplier's address",
                validate=validation.supplier_address_validation
            )]
            value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if value is not None:
                criteria = {"elements": event_logs.get_raw_materials_used_events,
                            "value": Web3.toChecksumAddress(value['Supplier']), "field": "supplier",
                            "operator": operator.eq, "event": True}
        elif action['field'] == choices[5]:  # TRANSFORMERS
            questions = [inquirer.Text(
                'Transformer',
                message="Transformer's address",
                validate=validation.transformer_address_validation
            )]
            value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if value is not None:
                criteria = {"elements": event_logs.get_raw_materials_used_events,
                            "value": Web3.toChecksumAddress(value['Transformer']), "field": "transformer",
                            "operator": operator.eq, "event": True}
        elif action['field'] == choices[6]:  # RAWMATERIALNAME
            questions = [inquirer.Text(
                'RawMaterial',
                message="Raw Material name",
                validate=validation.name_input_validation
            )]
            value = inquirer.prompt(questions, theme=load_theme_from_dict(theme))
            if value is not None:
                criteria = {"elements": event_logs.get_raw_materials_used_events, "value": value['RawMaterial'],
                            "field": "name", "operator": personalized_contains, "event": True}
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
                    print_products(results)
                    question = [inquirer.Text(
                        'PID',
                        message="Insert a product ID to see product details",
                        validate=validation.id_input_validation
                    )]
                    value = inquirer.prompt(question, theme=load_theme_from_dict(theme))
                    if value is not None:
                        detailed_print(int(value['PID']))
                elif action['action'] == choices[1]:
                    filter_products(results, and_filter)
                elif action['action'] == choices[2]:
                    filter_products(results, or_filter)
        elif criteria:
            print("\nNo products match the specified filter\n")
