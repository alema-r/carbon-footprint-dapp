"""
Module used to create contracts

"""
import json
import sys

from web3 import Web3


def build_user_contract(web3: Web3):
    """Creates the User smart contract.

    Args:
        web3 (Web3): a Web3 object

    Returns:
        web3.eth.contract: the user contract
    """
    # getting the address in which the contract is deployed
    with open("address.json", "r", encoding="utf-8") as file:
        contract_address_string = json.load(file)["address"]
    if contract_address_string == "":
        print("Contracts are not deployed correctly. Check the address.json file.")
        sys.exit(1)
    # getting the user contract interface in order to build user contract instance
    with open("solc_output/UserContract.json", "r", encoding="utf-8") as user_compiled:
        user_interface = json.load(user_compiled)
    # converting the address in checksum address in order to be compatible
    contract_address = web3.toChecksumAddress(contract_address_string)
    # creating user contract instance in order to interact with it
    user_contract = web3.eth.contract(
        address=contract_address, abi=user_interface["abi"]
    )
    return user_contract


def build_cf_contract(user_contract, web3: Web3):
    """Creates the CarbonFootprint smart contract.

    Args:
        user_contract (web3.eth.contract): the user contract
        web3 (Web3): a Web3 istance

    Returns:
        web3.eth.contract: the CarbonFootprint contract.
    """
    # getting the user contract interface in order to build Carboon FootPrint contract instance
    with open("solc_output/CFContract.json", "r", encoding="utf-8") as cf_compiled:
        cf_interface = json.load(cf_compiled)
    # creating carboon footprint contract instance in order to interact with it
    cf_contract = web3.eth.contract(
        address=user_contract.functions.CFaddress().call(), abi=cf_interface["abi"]
    )
    return cf_contract
