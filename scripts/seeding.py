#!/usr/bin/env python3
"""Script used to create a demo scenario on the blockchain.
"""
import json

from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3 import exceptions

BASE_URL = "http://127.0.0.1:2200"


class Bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def create_users(role: int):
    web3 = Web3(Web3.HTTPProvider(BASE_URL + str(role)))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    with open("../address.json", "r", encoding="utf-8") as file:
        address = json.load(file)["address"]
    with open(
        "../solc_output/UserContract.json", "r", encoding="utf-8"
    ) as user_compiled:
        user_interface = json.load(user_compiled)
    contract_address = Web3.toChecksumAddress(address)
    user_contract = web3.eth.contract(
        address=contract_address, abi=user_interface["abi"]
    )
    addresses = get_addresses(role)
    for address in addresses:
        web3.geth.personal.unlock_account(address, "")
        if user_contract.functions.getRole(address).call() == 0:
            # set account as web3 default account in order to accomplish transactions
            web3.eth.default_account = address
            # creating new user in the contract state, in the mapping associating address to role
            tx_hash = user_contract.functions.createUser(role).transact()
            # we wait for transaction receipt in order to do all transactions
            # because python execution is faster than transaction mining
            web3.eth.wait_for_transaction_receipt(tx_hash)
    return web3, user_contract


def get_addresses(role: int):
    web3 = Web3(Web3.HTTPProvider(BASE_URL + str(role)))
    if len(web3.geth.personal.list_wallets()) <= 1:
        web3.geth.personal.new_account("")
    return web3.geth.personal.list_accounts()


def create_rm(web3, user_contract, nome, lotto, cf, tr):
    try:
        tx_hash = user_contract.functions.createRawMaterials(nome, lotto, cf, tr).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(
            f"{Bcolors.OKGREEN}[RAW MATERIAL CREATED]{Bcolors.ENDC} {Bcolors.BOLD}{nome[0]}{Bcolors.ENDC}, lot: {lotto[0]}, cf: {cf[0]}"
        )
    except exceptions.ContractLogicError as e:
        print(f"{Bcolors.FAIL}[ERROR]{Bcolors.ENDC} {e}")


def mint_product(web3, user_contract, nome, rms):
    try:
        tx_hash = user_contract.functions.createProduct(nome, rms).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(
            f"{Bcolors.OKBLUE}[PRODUCT MINTED]{Bcolors.ENDC} {Bcolors.BOLD}{nome}{Bcolors.ENDC}"
        )
    except exceptions.ContractLogicError as e:
        print(f"{Bcolors.FAIL}[ERROR]{Bcolors.ENDC} {e}")


def add_cf(web3, user_contract, cf, p_id, ended):
    try:
        tx_hash = user_contract.functions.addTransformation(cf, p_id, ended).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(
            f"{Bcolors.OKCYAN}[TRANSFORMATION PERFORMED]{Bcolors.ENDC} added {cf} cf to Prodotto{p_id}"
        )
        if ended:
            print(f"{Bcolors.WARNING}[PRODUCT ENDED]{Bcolors.ENDC} Prodotto{p_id}")
    except exceptions.ContractLogicError as e:
        print(f"{Bcolors.FAIL}[ERROR]{Bcolors.ENDC} {e}")


def seeding(role, web3, user_contract):
    """
    Function that creates a demo scenario on blockchain with twenty-four raw materials, six products thirty
    transformations. If there is only one account stored in the node to which we are connected, it also creates another
    account on the node and registers it on the blockchain
    Args:
        role: role associated to the current node we are connected
    """
    addresses = get_addresses(role)
    if role == 1:
        transformer_addresses = get_addresses(2)
        print(f"{Bcolors.HEADER}CREATING RAW MATERIALS{Bcolors.ENDC}")
        for address in addresses:
            # creating twelve raw materials per supplier with standard name, lot and cf
            web3.eth.default_account = address
            for i in range(12):
                nome = [f"MateriaPrima{i % 4}"]
                lotto = [int(i // 4)]
                cf = [(i // 4) * 100 + (i % 4) * 10 + 10]
                tr = (
                    [transformer_addresses[0]]
                    if i % 2 == 0
                    else [transformer_addresses[1]]
                )
                # transaction to create raw materials on blockchain
                create_rm(web3, user_contract, nome, lotto, cf, tr)

    elif role == 2:
        print(f"{Bcolors.HEADER}MINTING PRODUCTS{Bcolors.ENDC}")
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
        print(f"{Bcolors.HEADER}STARTING TRANSFORMATIONS{Bcolors.ENDC}")
        # starting a cycle in which for every product are done five transformations.
        # product 3 and product 6 are marked as finished
        for i in range(1, 7):
            if i > 3:
                # setting as default account the second transformer in order to perform transactions
                web3.eth.default_account = addresses[1]
            for j in range(1, 6):
                if i in (3, 6) and j == 5:
                    add_cf(web3, user_contract, j * 5, i, True)
                else:
                    add_cf(web3, user_contract, j * 5, i, False)
    else:
        return


if __name__ == "__main__":
    web3_s, user_contract_s = create_users(1)
    web3_t, user_contract_t = create_users(2)
    seeding(1, web3_s, user_contract_s)
    seeding(2, web3_t, user_contract_t)
