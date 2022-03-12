from web3 import Web3
import json
import inquirer
baseURL = "http://127.0.0.1:2200"


def get_wallet():
    return inquirer.text(
        message="Insert your wallet address",
    )
    #Controllare l'autorizzazione dell'utente ovvero che il wallet inserito sia effettivamente
    # un wallet prensete sulla blockchain e che sia del guisto ruolo


def connect(role):
    URL = baseURL + str(role)
    web3 = Web3(Web3.HTTPProvider(URL))
    #print(web3.isConnected())
    abi = json.loads(abi_string)
    address = web3.toChecksumAddress(usercontractAddress)
    contract = web3.eth.contract(address=address, abi=abi)
    user_adress = web3.toChecksumAddress(get_wallet())
    web3.eth.defaultAccount = user_adress
    return contract, user_adress
