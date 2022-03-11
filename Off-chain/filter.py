import operator

#Ritorna la lista degli Id dei prodotti che rispettano il filtro specificato
def simpleFilter(elements, value, field = 1, op = operator.eq):
    result = []
    for e in elements:
        if(op(e[field], value)):
            result.append(e[0])
    return result

def orFilter(elements_list, values, fields, ops):
    result = []
    for i in range(0, len(fields)):
        result += simpleFilter(elements_list[i], values[i], fields[i], ops[i])
    return list(set(result))

def andFilter(elements_list, values, fields, ops):
    result = simpleFilter(elements_list[0], values[0], fields[0], ops[0])
    for i in range(1, len(fields)):
        temp = simpleFilter(elements_list[i], values[i], fields[i], ops[i])
        for e in result:
            if e not in temp:
                result.remove(e)
    return result