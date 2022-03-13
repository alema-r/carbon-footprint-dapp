from web3 import Web3
import json
import inquirer

baseURL = "http://127.0.0.1:2200"
with open("../solc_output/UserContract.json", "r") as user_compiled:
    user_interface = json.load(user_compiled)
with open("../solc_output/CFContract.json", "r") as cf_compiled:
    cf_interface = json.load(cf_compiled)

abi_user = user_interface["abi"]
bytecode_user = user_interface["evm"]["bytecode"]["object"]
abi_cf = cf_interface["abi"]


def get_wallet():
    return inquirer.text(
        message="Insert your wallet address",
    )


def connect(role):
    URL = baseURL + str(role)
    web3 = Web3(Web3.HTTPProvider(URL))
    #print(web3.isConnected())
    abi = json.loads(abi_string)
    address = web3.toChecksumAddress(usercontractAddress)
    contract = web3.eth.contract(address=address, abi=abi)
    web3.eth.defaultAccount = web3.toChecksumAddress(get_wallet())
    return contract
