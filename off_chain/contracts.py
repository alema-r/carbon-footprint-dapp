"""
Module used to interact with contracts deployed on the blockchain.
First, import this module, then access the contract by doing:
`contracts.user_contract` or `contracts.cf_contract`.

Since every subsequent `import` after the first uses the cached module
instead of re-evaluating it, it is guaranteed that every module that import
contracts, refer to the same instance.
"""
import json

from web3 import Web3


def build_user_contract(web3: Web3):
    # getting the address in which the contract is deployed
    with open("address.json", "r") as file:
        contract_address_string = json.load(file)["address"]
    # getting the user contract interface in order to build user contract instance
    with open("solc_output/UserContract.json", "r") as user_compiled:
        user_interface = json.load(user_compiled)
    # converting the address in checksum address in order to be compatible
    contract_address = web3.toChecksumAddress(contract_address_string)
    # creating user contract instance in order to interact with it
    user_contract = web3.eth.contract(
        address=contract_address, abi=user_interface["abi"]
    )
    return user_contract


def build_cf_contract(user_contract, web3: Web3):
    # getting the user contract interface in order to build Carboon FootPrint contract instance
    with open("solc_output/CFContract.json", "r") as cf_compiled:
        cf_interface = json.load(cf_compiled)
    # creating carboon footprint contract instance in order to interact with it
    cf_contract = web3.eth.contract(
        address=user_contract.functions.CFaddress().call(), abi=cf_interface["abi"]
    )
    return cf_contract
