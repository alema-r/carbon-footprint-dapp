from web3 import Web3
import json
import inquirer
baseURL = "http://127.0.0.1:22000"
usercontractAddress = "0x1349F3e1B8D71eFfb47B840594Ff27dA7E603d17"
abi_user_contract = '[{"inputs":[{"internalType":"address","name":"defaultSupplier","type":"address"},{"internalType":"address","name":"defaultTransformer","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"enum User.Role","name":"role","type":"uint8"}],"name":"newUser","type":"event"},{"inputs":[],"name":"CFaddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"carbon_fp","type":"uint16"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bool","name":"isEnded","type":"bool"}],"name":"addTransformation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"product_name","type":"string"},{"internalType":"string[]","name":"raw_material","type":"string[]"},{"internalType":"uint256[]","name":"lots","type":"uint256[]"},{"internalType":"uint256","name":"carbon_fp","type":"uint256"}],"name":"createProduct","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint8","name":"role","type":"uint8"}],"name":"createUser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getProducts","outputs":[{"components":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"address","name":"currentOwner","type":"address"},{"internalType":"uint256","name":"CF","type":"uint256"},{"internalType":"bool","name":"ended","type":"bool"}],"internalType":"struct ProductLibrary.Product[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getRole","outputs":[{"internalType":"enum User.Role","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRole","outputs":[{"internalType":"enum User.Role","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferCP","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

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
    abi = json.loads(abi_user_contract)
    address = web3.toChecksumAddress(usercontractAddress)
    contract = web3.eth.contract(address=address, abi=abi)
    user_adress = web3.toChecksumAddress(get_wallet())
    web3.eth.defaultAccount = user_adress
    return contract, user_adress
