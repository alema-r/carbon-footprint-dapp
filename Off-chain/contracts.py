"""
Module used to interact with contracts deployed on the blockchain.
First, import this module, then access the contract by doing:
`contracts.user_contract` or `contracts.cf_contract`.

Since every subsequent `import` after the first uses the cached module
instead of re-evaluating it, it is guaranteed that every module that import
contracts, refer to the same instance.
"""
import os
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
os.chdir(str(os.getcwd())+"/Off-chain/")
with open("address.json", "r") as file:
    address = json.load(file)["address"]
with open("../solc_output/UserContract.json", "r") as user_compiled:
    user_interface = json.load(user_compiled)

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:22000"))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

if address == "":
    # Gli address dei nodi sono uguali per tutti i 3 nodes quickstart creati con quorum-wizard
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
    with open("address.json", "w") as file:
        json_address = dict(address=user_contract.address)
        json.dump(json_address, file)

else:
    contract_address = web3.toChecksumAddress(address)
    user_contract = web3.eth.contract(
        address=contract_address, abi=user_interface["abi"]
    )

with open("../solc_output/CFContract.json", "r") as cf_compiled:
    cf_interface = json.load(cf_compiled)

cf_contract = web3.eth.contract(
    address=user_contract.functions.CFaddress().call(), abi=cf_interface["abi"]
)
