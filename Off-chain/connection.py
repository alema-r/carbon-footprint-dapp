from web3 import Web3

baseURL = "http://127.0.0.1:2200"


def connect(role):
    URL = baseURL + str(role)
    web3 = Web3(Web3.HTTPProvider(URL))
    print(web3.isConnected())