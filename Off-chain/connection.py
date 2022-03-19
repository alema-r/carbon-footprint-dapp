import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

BASE_URL = "http://127.0.0.1:2200"


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


def connect(role):
    url = BASE_URL + str(role)
    web3 = Web3(Web3.HTTPProvider(url))
    user_contract = UserContract(web3=web3)
    cf_contract = web3.eth.contract(
        address=user_contract.functions.CFaddress().call(), abi=cf_interface["abi"]
    )
    return web3, user_contract, cf_contract
