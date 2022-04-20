import json

from web3 import Web3
from web3.middleware import geth_poa_middleware

BASE_URL = "http://127.0.0.1:2200"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_addresses(role: int):
    web3 = Web3(Web3.HTTPProvider(BASE_URL + str(role)))
    if len(web3.geth.personal.list_wallets()) <= 1:
        web3.geth.personal.new_account('')
    return web3.geth.personal.list_accounts()

def create_rm(web3, user_contract, nome, lotto, cf, tr):
    tx_hash = user_contract.functions.createRawMaterials(nome, lotto, cf, tr).transact()
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"{bcolors.OKGREEN}[RAW MATERIAL CREATED]{bcolors.ENDC} {bcolors.BOLD}{nome[0]}{bcolors.ENDC}, lot: {lotto[0]}, cf: {cf[0]}")

def mint_product(web3, user_contract, nome, rms):
    tx_hash = user_contract.functions.createProduct(nome, rms).transact()
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"{bcolors.OKBLUE}[PRODUCT MINTED]{bcolors.ENDC} {bcolors.BOLD}{nome}{bcolors.ENDC}")

def add_cf(web3, user_contract, cf, p_id, ended):
    tx_hash = user_contract.functions.addTransformation(cf, p_id, ended).transact()
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"{bcolors.OKCYAN}[TRANSFORMATION PERFORMED]{bcolors.ENDC} added {cf} cf to Prodotto{p_id}")
    if ended:
        print(f"{bcolors.WARNING}[PRODUCT ENDED]{bcolors.ENDC} Prodotto{p_id}")

def seeding(role):
    """
    Function that creates a demo scenario on blockchain with twenty-four raw materials, six products thirty
    transformations. If there is only one account stored in the node to which we are connected, it also creates another
    account on the node and registers it on the blockchain
    Args:
        role: role associated to the current node we are connected
    """
    # creating web3 connection
    web3 = Web3(Web3.HTTPProvider(BASE_URL + str(role)))
    # injects proof of authority middleware in order to accomplish transaction
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    # retrieving address of deployment and abi of the user contract in order to build it
    with open("address.json", "r") as file:
        address = json.load(file)["address"]
    with open("solc_output/UserContract.json", "r") as user_compiled:
        user_interface = json.load(user_compiled)
    # converting address into checksum address
    contract_address = web3.toChecksumAddress(address)
    # building user contract instance
    user_contract = web3.eth.contract(
        address=contract_address, abi=user_interface["abi"]
    )
    addresses = get_addresses(role)
    if role == 1:
        transformer_addresses = get_addresses(2)
        print(f'{bcolors.HEADER}CREATING RAW MATERIALS{bcolors.ENDC}')
        for address in addresses:
            #  if supplier is not registered, we create the account inside the state of the contract
            web3.geth.personal.unlock_account(address, '')
            if user_contract.functions.getRole(address).call() == 0:
                # set account as web3 default account in order to accomplish transactions
                web3.eth.default_account = address
                # creating new user in the contract state, in the mapping associating address to role
                tx_hash = user_contract.functions.createUser(1).transact()
                # we wait for transaction receipt in order to do all transactions because python execution is faster
                # than transaction mining
                web3.eth.wait_for_transaction_receipt(tx_hash)

            web3.eth.default_account = address
            # creating twelve raw materials per supplier with standard name, lot and cf
            for i in range(12):
                nome = [f"MateriaPrima{i % 4}"]
                lotto = [int(i // 4)]
                cf = [(i // 4)*100 + (i % 4)*10 + 10]
                tr = [transformer_addresses[0]] if i % 2 == 0 else [transformer_addresses[1]]
                # transaction to create raw materials on blockchain
                create_rm(web3, user_contract, nome, lotto, cf, tr)
        

    elif role == 2:
        for address in addresses:
            web3.geth.personal.unlock_account(address, '')
            # same logic as supplier applied to transformer
            if user_contract.functions.getRole(address).call() == 0:
                web3.eth.default_account = address
                tx_hash = user_contract.functions.createUser(2).transact()
                web3.eth.wait_for_transaction_receipt(tx_hash)

        print(f'{bcolors.HEADER}MINTING PRODUCTS{bcolors.ENDC}')
        # setting as default account the first transformer
        web3.eth.default_account = addresses[0]
        mint_product(web3, user_contract, "Prodotto1", [0, 20, 8])
        mint_product(web3, user_contract, "Prodotto2", [2, 22, 10])
        mint_product(web3, user_contract, "Prodotto3", [6, 12, 18])
        
        # setting as default account the second transformer
        web3.eth.default_account = addresses[1]
        mint_product(web3, user_contract, "Prodotto4", [15, 3, 5])
        mint_product(web3, user_contract, "Prodotto5", [11, 21, 17])
        mint_product(web3, user_contract, "Prodotto6", [9, 1, 19])
        
        # setting as default account the first transformer again
        web3.eth.default_account = addresses[0]
        print(f'{bcolors.HEADER}STARTING TRANSFORMATIONS{bcolors.ENDC}')
        # starting a cycle in which for every product are done five transformations.
        # product 3 and product 6 are marked as finished
        for i in range(1, 7):
            if i > 3:
                # setting as default account the second transformer in order to perform transactions
                web3.eth.default_account = addresses[1]
            for j in range(1, 6):
                if (i == 3 or i == 6) and j == 5:
                    add_cf(web3, user_contract, j*5, i, True)
                else:
                    add_cf(web3, user_contract, j*5, i, False)
    else:
        return

if __name__ == "__main__":
    seeding(1)
    seeding(2)
