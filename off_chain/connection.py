"""
Modules that ask user's role and initialize connection to the node
corresponding to user role inserted. Here it is also injected proof
of authority middleware in order to accomplish transaction on the blockcchain.
"""
from web3 import Web3
from web3.middleware import geth_poa_middleware

BASE_URL = "http://127.0.0.1:2200"


def connection(role: int):
    """Connects a user to a specific node.

    Args:
        role (int): the role of the user

    Returns:
        (Web3): a web3 object
    """
    # creating the node address url with the given role
    url = BASE_URL + str(role)
    # creates web3 connection to the selected node
    web3 = Web3(Web3.HTTPProvider(url))
    # injects proof of authority middleware to complete transactions
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3
