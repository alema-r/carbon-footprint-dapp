from web3 import Web3
import web3

# TODO: gestire le eccezioni che arrivano dalla blockchain, in particolare quelle dovute alla duplicazione delle materie prime presenti

"""
Funzione che controlla l'input che viene mandato sulla blockchain e poi fa la chiamata alla funzione del contratto.
"""
'''
def create_product_on_blockchain(contract, product_name: str, raw_materials, carbon_fp: int):
    #sanificazione dell'input
    raw_materials_ok = check_raw_material(raw_materials)
    if (len(product_name)>0) & (raw_materials_ok) & (carbon_fp>0):
        raw_materials_name_list = [raw_material.get_name() for raw_material in raw_materials]
        raw_materials_lot_list = [raw_material.get_lot() for raw_material in raw_materials]
        try:
            # Chiamata alla funzione per creare un nuovo prodotto sulla blockchain
            # TODO: imparare a gestire le eccezioni che arrivano dalla blockchain soprattutto quella riguardante carbonfootprin e lotto già inseriti
            contract.functions.createProduct(product_name, raw_materials_name_list, raw_materials_lot_list, carbon_fp).transact()
        except:
            raise Exception("Unable to call createProduct function on blockchain")
    else:
        raise Exception("Improper input's formats")
        pass
'''
def create_raw_materials_on_blockchain(contract, raw_materials):
    '''
    Inserisce un nuovo token materia prima nella blockchain 

    Keyword arguments:
    contract -- l'istanza del contratto chiamato sulla blockchain
    raw_materials -- lista di oggetti materie prime che contengono tutte le informazioni sulle materie prima da caricare sulla blockchain
    carbon_fp -- Carbon footprint associata alla materia prima che si sta inserendo
    '''
    try:
        raw_materials_name_list = [raw_material.get_name() for raw_material in raw_materials]
        raw_materials_lot_list = [raw_material.get_lot() for raw_material in raw_materials]
        raw_materials_cf_list = [raw_material.get_cf() for raw_material in raw_materials]
        contract.functions.createRawMaterials(raw_materials_name_list, raw_materials_lot_list, raw_materials_cf_list).transact()
    except Exception as e:
        if (e.__str__ == "Il numero delle materie prime non corrispone al numero di lotti") or (e.__str__ == "Il numero delle materie prime non corrisponde al numero delle carbon footprint") or (e.__str__ == "Hai già inserito questo lotto di questa materia prima"):
            raise e
        else:
            raise Exception("Errore nel caricamento della materia prima")


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
