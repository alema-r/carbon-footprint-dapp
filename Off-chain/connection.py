from attr import validate
from sklearn.linear_model import ARDRegression
from web3 import Web3
import json
import inquirer
from Utils import address_validation
import sys

# TODO: aggiungere l'address del contratto user quando lo creo.
usercontractAddress = ""
baseURL = "http://127.0.0.1:2200"
with open("../solc_output/UserContract.json", "r") as user_compiled:
    user_interface = json.load(user_compiled)
with open("../solc_output/CFContract.json", "r") as cf_compiled:
    cf_interface = json.load(cf_compiled)

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
