import os
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

baseURL = "http://127.0.0.1:2200"


def seeding(role):
    web3 = Web3(Web3.HTTPProvider(baseURL + str(role)))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    os.chdir(str(os.getcwd()) + "/Off-chain/")
    with open("address.json", "r") as file:
        address = json.load(file)["address"]
    with open("../solc_output/UserContract.json", "r") as user_compiled:
        user_interface = json.load(user_compiled)
    contract_address = web3.toChecksumAddress(address)
    user_contract = web3.eth.contract(
        address=contract_address, abi=user_interface["abi"]
    )
    if len(web3.geth.personal.list_wallets()) <= 1:
        address_1 = web3.geth.personal.new_account('')
        web3.geth.personal.unlock_account(address_1, '')
    addresses = web3.geth.personal.list_accounts()
    if role == 1:
        j = 0
        for address in addresses:
            if user_contract.functions.getRole(address).call() == 0:
                web3.eth.default_account = address
                tx_hash = user_contract.functions.createUser(1).transact()
                web3.eth.wait_for_transaction_receipt(tx_hash)
        print('Creating raw_materials')
        for address in addresses:
            web3.eth.default_account = address
            print(web3.eth.default_account)
            for i in range(1, 13):
                nome = [f"MateriaPrima{i % 4}"]
                lotto = [int(i // 4)]
                cf = [(i//4)*100+(i%4)*10]
                tx_hash = user_contract.functions.createRawMaterials(nome, lotto, cf).transact()
                web3.eth.wait_for_transaction_receipt(tx_hash)
    elif role == 2:
        k = 0
        for address in addresses:
            if user_contract.functions.getRole(address).call() == 0:
                web3.eth.default_account = address
                tx_hash = user_contract.functions.createUser(2).transact()
                web3.eth.wait_for_transaction_receipt(tx_hash)
        web3.eth.default_account = addresses[0]
        tx_hash = user_contract.functions.createProduct("Prodotto1", [0, 23, 7]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_hash = user_contract.functions.createProduct("Prodotto2", [1, 22, 20]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_hash = user_contract.functions.createProduct("Prodotto3", [5, 9, 18]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        web3.eth.default_account = addresses[1]
        tx_hash = user_contract.functions.createProduct("Prodotto4", [15, 3, 4]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_hash = user_contract.functions.createProduct("Prodotto5", [14, 21, 17]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_hash = user_contract.functions.createProduct("Prodotto6", [11, 16, 19]).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        web3.eth.default_account = addresses[0]
        print("starting Transformations")
        for i in range(1, 7):
            if i > 3:
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
    seeding(0)
