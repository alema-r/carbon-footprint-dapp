#!/usr/bin/env python3
"""Script used to deploy contracts on the blockchain.
"""

import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

# getting the address of the contracts in the address JSON file
with open("../address.json", "r", encoding="utf-8") as file:
    address = json.load(file)["address"]
# getting the user contract interface in order to build user contract instance
with open("../solc_output/UserContract.json", "r", encoding="utf-8") as user_compiled:
    user_interface = json.load(user_compiled)

# creating web3 connection to deploy contracts on the blockchain
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:22000"))
# injects proof of authority middleware to complete transactions
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# controlling if address.json file is empty or if at the address saved in json file there are no
# deployed contracts
if address == "" or web3.eth.get_code(address) != b"":
    # Initializing default supplier and default Transformer instances with
    node2_wallet = web3.toChecksumAddress("0xca843569e3427144cead5e4d5999a3d0ccf92b8e")
    node3_wallet = web3.toChecksumAddress("0x0fbdc686b912d7722dc86510934589e0aaf3b55a")
    web3.eth.default_account = web3.eth.accounts[0]
    User = web3.eth.contract(
        abi=user_interface["abi"],
        bytecode=user_interface["evm"]["bytecode"]["object"],
    )
    tx_hash = User.constructor(
        defaultSupplier=node2_wallet, defaultTransformer=node3_wallet
    ).transact()
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    user_contract = web3.eth.contract(
        address=tx_receipt.contractAddress, abi=user_interface["abi"]
    )
    with open("../address.json", "w") as file:
        json_address = dict(address=user_contract.address)
        json.dump(json_address, file)
else:
    print("Contracts are already deployed. You can start using the application")
