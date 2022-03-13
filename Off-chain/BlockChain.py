from web3 import Web3
# TODO:Quale è la relazione fra materie prime e lotti, come li devo correlare???

def check_raw_material(raw_materials):
    is_ok = True
    # Si controlla che tutti gli elementi dell'array siano effettivamente delle stringe e che ci sia almeno una materia prima
    for material in raw_materials:
        if isinstance(material, str) & material:
            pass
        else:
            is_ok = False
    # Si controlla che ci sia almeno una materia prima    
    if len(raw_materials) == 0:
        is_ok = False
    
    return is_ok

def check_lots(lots):
    is_ok = True
    # Si controlla che tutti gli elementi nell'array siano effettivamente numeri interi e siano positivi
    for lot in lots:
        if isinstance(lot, int) & lot >= 0:
            pass
        else:
            is_ok = False
    # Si controlla che ci sia almeno un lotto di materie prime per creare il prodotto
    if len(lots) == 0:
        is_ok = False

    return is_ok

"""
Funzione che controlla l'input che viene mandato sulla blockchain e poi fa la chiamata alla funzione del contratto.
"""
def create_product_on_blockchain(contract, product_name, raw_materials, lots, carbon_fp):
    #sanificazione dell'input
    raw_materials_ok = check_raw_material(raw_materials)
    lots_ok= check_lots(lots)
    if type(product_name) is str & product_name &  raw_materials_ok & lots_ok &  isinstance(carbon_fp, int) & carbon_fp:
        try:
            # Chiamata alla funzione per creare un nuovo prodotto sulla blockchain
            # TODO: imparare a gestire le eccezioni che arrivano dalla blockchain soprattutto quella riguardante carbonfootprin e lotto già inserito

            contract.functions.createProduct(product_name, raw_materials, lots, carbon_fp).transact()
        except:
            raise Exception("Unable to call createProduct function on blockchain")
    else:
        # TODO: chiedere come inserire una eccezione migliore.
        raise Exception("Improper input's formats")

def transfer_cp(contract, recipient, token_id):
    try:
        # Funzione che trasferisce la CP al trasformatore.
        contract.functions.transferCP(recipient, token_id).transact()
    except:
        raise Exception("Token transfer error")

def add_transformation_on_blockchain(contract, carb_foot, product_id, is_the_final):
    '''This function connects to the blockchain to add a new transformation
    
    Keyword arguments:
    contract -- the instance of Contract needed to connect to the blockchain
    carb_foot -- the value of the carbon footprint 
    product_id -- the id of the product to which a new transformation needs to be added
    is_the_final -- boolean that indicates if this is the final transformation of the production chain'''
    try:
        contract.functions.addTransformation(
            carb_foot,  product_id, is_the_final).transact()
    except:
        raise Exception
        
def transfer_product_on_blockchain(contract, transfer_to, product_id):
    '''This function connects to the blockchain to transfer the ownership of a product
    
    Keyword arguments:
    contract -- the instance of Contract needed to connect to the blockchain
    transfer_to -- the adress of the user to whom the product ownership needs to be transfered
    product_id -- the id of the product to transfer
    '''
    try:
        contract.functions.transferCP(transfer_to, product_id).transact()
    except:
        raise Exception
