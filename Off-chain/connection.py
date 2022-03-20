from attr import validate
from sklearn.linear_model import ARDRegression
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import inquirer
from Utils import address_validation
import sys

BASE_URL = "http://127.0.0.1:22000"


class UserContract(object):
    """
    A singleton class for the `User` contract.
    """

    def __new__(cls, web3: Web3):
        """
        Creates a new istance of the class if it doesn't exists.
        Checks if there is an address in the file address.json. If not it 
        creates the contract and it save the address for subsequent uses.
        Returns a `web3._utils.datatypes.Contract`
        """
        if not hasattr(cls, "instance"):
            with open("address.json", 'r') as file:
                address = json.load(file)['address']
            with open("../solc_output/UserContract.json", "r") as user_compiled:
                user_interface = json.load(user_compiled)
            if address == "":
                # Gli address dei nodi sono uguali per tutti i 3 nodes quickstart creati con quorum-wizard
                node2_wallet = web3.toChecksumAddress(
                    "0xca843569e3427144cead5e4d5999a3d0ccf92b8e"
                )
                node3_wallet = web3.toChecksumAddress(
                    "0x0fbdc686b912d7722dc86510934589e0aaf3b55a"
                )
                web3.middleware_onion.inject(geth_poa_middleware, layer=0)
                web3.eth.default_account = web3.eth.accounts[0]
                User = web3.eth.contract(
                    abi=user_interface["abi"],
                    bytecode=user_interface["evm"]["bytecode"]["object"],
                )
                tx_hash = User.constructor(
                    defaultSupplier=node2_wallet, defaultTransformer=node3_wallet
                ).transact()
                tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                user = web3.eth.contract(
                    address=tx_receipt.contractAddress, abi=user_interface["abi"]
                )
                with open("address.json", "w") as file:
                    json_address = dict(address=user.address)
                    json.dump(json_address, file)
                cls.instance = user
            else:
                contract_address = web3.toChecksumAddress(address)
                user = web3.eth.contract(address=contract_address, abi=user_interface["abi"])
                cls.instance = user
        return cls.instance

with open("../solc_output/CFContract.json", "r") as cf_compiled:
    cf_interface = json.load(cf_compiled)

"""
abi_user = user_interface["abi"]
bytecode_user = user_interface["evm"]["bytecode"]["object"]
abi_cf = cf_interface["abi"]


def get_wallet(contract, role):
    adress = inquirer.text(
        message="Insert your wallet address"
    )
    while (not address_validation(contract, adress, role)):
        print("The inserted address is not valid. Try again.")
        choice = inquirer.list_input(
            choices=["Input the address", "Quit"]
        )
        if choice == "Input the address":
            adress = inquirer.text(
                message="Insert your wallet address"
            )
        else:
            sys.exit()
    #Controllare l'autorizzazione dell'utente ovvero che il wallet inserito sia effettivamente
    # un wallet prensete sulla blockchain e che sia del guisto ruolo


def connect(role):
    URL = baseURL + str(role)
    web3 = Web3(Web3.HTTPProvider(URL))
    #print(web3.isConnected())
    abi = json.loads(abi_user)
    address = web3.toChecksumAddress(usercontractAddress)
    contract = web3.eth.contract(address=address, abi=abi)
    user_address = web3.toChecksumAddress(get_wallet(contract, role))
    web3.eth.defaultAccount = user_address
    return contract, user_address
"""

def connect(role):
    url = BASE_URL + str(role)
    web3 = Web3(Web3.HTTPProvider(url))
    user_contract = UserContract(web3=web3)
    cf_contract = web3.eth.contract(
        address=user_contract.functions.CFaddress().call(), abi=cf_interface["abi"]
    )
    return web3, user_contract, cf_contract
