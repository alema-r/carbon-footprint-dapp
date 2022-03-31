import operator
import inquirer     #TEST
import BlockChain   #TEST
import event_logs   #TEST
import Utils        #TEST
import Transformer  #TEST
import Supplier  #TEST


def simpleFilter(function, value, field, op=operator.eq, fromEvent=False):
    elements = function()
    result = []
    if fromEvent:
        for e in elements:
            if op(e["args"][field], value):
                result.append(e["args"]["pId"])
    else:
        for e in elements:
            if op(getattr(e, field), value):
                result.append(e.productId)
    return result


def orFilter(criteria):
    result = []
    for c in criteria:
        result += simpleFilter(c["elements"], c["value"], c["field"], c["operator"], c["event"])
    return list(set(result))


def andFilter(criteria):
    result = simpleFilter(criteria[0]["elements"], criteria[0]["value"], criteria[0]["field"], criteria[0]["operator"], criteria[0]["event"])
    for i in range(1, len(criteria)):
        temp = simpleFilter(criteria[i]["elements"], criteria[i]["value"], criteria[i]["field"], criteria[i]["operator"], criteria[i]["event"])
        temp2 = result.copy()
        for e in temp2:
            if e not in temp:
                result.remove(e)
    return result

''''''

def select_operator():
    choices = ["Equal", "Greater", "Lower"]
    action = inquirer.list_input(
        message="Select an operator",
        choices=choices
    )
    if action == choices[0]:    #ALTRI OPERATORI
        op = operator.eq
    elif action == choices[1]:
        op = operator.gt
    elif action == choices[2]:
        op = operator.lt
    return op

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
    try:
        int_id=int(current)
    except:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: ID must be an integer greater than 0')
    if int_id < 1:
        raise inquirer.errors.ValidationError('', reason = 'Invalid input: ID must be an integer greater than 0')
    return True


if __name__ == "__main__":
    while True:
        filtro = []
        error = True
        while error:
            error = False
            choices = ["Id", "Name", "Owner", "CF", "Ended", "Supplier", "Transformer",
                       "Raw Material"]
            action = inquirer.list_input(
                message="Select a field",
                choices=choices
            )
            if action == choices[0]:    #ID
                value = int(inquirer.text(
                    message="ID: ",
                    validate=id_input_validation
                ))
                op = select_operator()
                filtro.append({"elements" : BlockChain.get_all_products,"value" : value, "field" : "productId","operator" : op,"event" : False})
            elif action == choices[1]:      #NAME
                value = inquirer.text(
                    message="Name: ",
                    validate=Transformer.new_product_name_input_validation
                )
                filtro.append({"elements" : BlockChain.get_all_products,"value" : value, "field" : "name","operator" : operator.eq,"event" : False})
            elif action == choices[2]:      #OWNER
                value = inquirer.text(
                    message="Owner's address: ",
                    validate=Utils.address_validation
                )
                filtro.append({"elements" : BlockChain.get_all_products,"value" : value,"field" : "address","operator" : operator.eq,"event" : False})
            elif action == choices[3]:      #CF
                value = int(inquirer.text(
                    message="CF value: ",
                    validate=Utils.carbon_fp_input_validation
                ))
                op = select_operator()
                filtro.append({"elements" : BlockChain.get_all_products,"value" : value, "field" : "CF","operator" : op,"event" : False})
            elif action == choices[4]:      #ISENDED
                choices = ["True", "False"]
                action = inquirer.list_input(
                    message="Is it ended?",
                    choices=choices
                )
                if action == choices[0]:
                    # value = True
                    filtro.append({"elements" : BlockChain.get_all_products, "value" : True, "field" : "isEnded", "operator" : operator.eq, "event" : False})
                else:
                    # value = False
                    filtro.append({"elements" : BlockChain.get_all_products, "value" : False, "field" : "isEnded", "operator" : operator.eq, "event" : False})
            elif action == choices[5]:      #SUPPLIERS
                value = inquirer.text(
                    message="Supplier's address: ",
                    #validate=Utils.address_validation   #controllo ruolo supplier?
                )
                filtro.append({"elements" : event_logs.get_raw_materials_used_events, "value" : value, "field" : "supplier", "operator" : operator.eq, "event" : True})
            elif action == choices[6]:      #TRANSFORMERS
                value = inquirer.text(
                    message="Transformer's address: ",
                    #validate=Utils.address_validation  # controllo ruolo transformer?
                )
                filtro.append({"elements" : event_logs.get_raw_materials_used_events, "value" : value, "field" : "transformer", "operator" : operator.eq, "event" : True})
            elif action == choices[7]:      #RAWMATERIALNAME
                value = inquirer.text(
                    message="Raw Material name: ",
                    validate=Supplier.raw_material_name_input_validation
                )
                filtro.append({"elements" : event_logs.get_raw_materials_used_events, "value" : value, "field" : "name", "operator" : operator.eq, "event" : True})
            choices = ["Continue", "Stop"]
            action = inquirer.list_input(
                message="Do you want to add another search criteria?",
                choices=choices
            )
            if action == choices[0]:
                error = True
            elif action == choices[1]:
                if len(filtro) > 1:
                    choices = ["AND", "OR"]
                    action = inquirer.list_input(
                        message="Filter Logic: ",
                        choices=choices
                    )
                    if action == choices[0]:
                        print(andFilter(filtro))
                    elif action == choices[1]:
                        print(orFilter(filtro))
                else:
                    print(simpleFilter(filtro[0]["elements"], filtro[0]["value"], filtro[0]["field"], filtro[0]["operator"], filtro[0]["event"]))
