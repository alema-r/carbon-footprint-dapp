import json
import sys

from web3 import Web3
from web3.middleware import geth_poa_middleware

baseURL = "http://127.0.0.1:2200"


def seeding(role):
    """
    Function that creates a demo scenario on blockchain with twenty-four raw materials, six products thirty
    transformations. If there is only one account stored in the node to which we are connected, it also creates another
    account on the node and registers it on the blockchain
    Args:
        role: role associated to the current node we are connected
    """
    # creating web3 connection
    web3 = Web3(Web3.HTTPProvider(baseURL + str(role)))
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
    # if there is only one account on the node we create another account
    if len(web3.geth.personal.list_wallets()) <= 1:
        # creating new account on blockchain
        web3.geth.personal.new_account('')
    # getting all accounts on the current node
    addresses = web3.geth.personal.list_accounts()
    if role == 1:
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
        print('Creating raw_materials')
        for address in addresses:
            web3.eth.default_account = address
            # creating twelve raw materials per supplier with standard name, lot and cf
            for i in range(0, 12):
                nome = [f"MateriaPrima{i % 4}"]
                lotto = [int(i // 4)]
                cf = [(i // 4)*100 + (i % 4)*10 + 10]
                # transaction to create raw materials on blockchain
                tx_hash = user_contract.functions.createRawMaterials(nome, lotto, cf).transact()
                web3.eth.wait_for_transaction_receipt(tx_hash)
    elif role == 2:
        for address in addresses:
            web3.geth.personal.unlock_account(address, '')
            # same logic as supplier applied to transformer
            if user_contract.functions.getRole(address).call() == 0:
                web3.eth.default_account = address
                tx_hash = user_contract.functions.createUser(2).transact()
                web3.eth.wait_for_transaction_receipt(tx_hash)
        # setting as default account the first transformer
        web3.eth.default_account = addresses[0]
        # we mint six products and for all transactions we wait for receipt in order to confirm transactions mining
        tx_hash = user_contract.functions.createProduct("Prodotto1", [0, 23, 7]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_hash = user_contract.functions.createProduct("Prodotto2", [1, 22, 20]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_hash = user_contract.functions.createProduct("Prodotto3", [5, 9, 18]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        # setting as default account the second transformer
        web3.eth.default_account = addresses[1]
        tx_hash = user_contract.functions.createProduct("Prodotto4", [15, 3, 4]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_hash = user_contract.functions.createProduct("Prodotto5", [14, 21, 17]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_hash = user_contract.functions.createProduct("Prodotto6", [11, 16, 19]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        # setting as default account the first transformer again
        web3.eth.default_account = addresses[0]
        print("starting Transformations")
        # starting a cycle in which for every product are done five transformations.
        # product 3 and product 6 are marked as finished
        for i in range(1, 7):
            if i > 3:
                # setting as default account the second transformer in order to perform transactions
                web3.eth.default_account = addresses[1]
            for j in range(1, 6):
                print("prodotto " + str(i) + " trasformazione: " + str(j))
                if (i == 3 or i == 6) and j == 5:
                    tx_hash = user_contract.functions.addTransformation(j * 5, i, True).transact()
                    web3.eth.wait_for_transaction_receipt(tx_hash)
                else:
                    tx_hash = user_contract.functions.addTransformation(j * 5, i, False).transact()
                    web3.eth.wait_for_transaction_receipt(tx_hash)
    else:
        return


if __name__ == "__main__":
    user_role = -1
    try:
        user_role = int(sys.argv[1])
    except ValueError as e:
        print(e)
        exit(user_role)
    roles = [0, 1, 2]
    if user_role in roles:
        seeding(user_role)
    else:
        print("Incorrect role provided. Seeding operation failed")
