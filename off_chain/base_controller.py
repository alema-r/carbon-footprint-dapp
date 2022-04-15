from functools import singledispatch
from eth_typing import ChecksumAddress
from typing import List
from web3 import Web3

from off_chain import contracts
from off_chain import event_logs
from off_chain.models import Product, RawMaterial, Transformation


class BlockChain:
    def __init__(self, web3: Web3):
        self.user_contract = contracts.build_user_contract(web3)
        self.event_logs = event_logs.EventLogs(contracts.build_cf_contract(self.user_contract, web3))

    def set_account_as_default(self, web3: Web3, user_role: int, address: str) -> ChecksumAddress:
        """
        Function used to check if user address corresponds to the given role and set current user address as
        default web3 account in order to accomplish transactions
        Args:
            web3: (Web3): instance of web3 connection to the blockchain
            user_role: (int): the integer identifier of the role chose by the current user
            address: (Address): address of current logged user

        Returns:
            address: (Address): validated address of the current user

        Raises:
            Exception: Custom general error raised if a non planned error occurs

        """
        try:
            # Checking for correct account format
            account = web3.toChecksumAddress(address)
            # If the account is inside the list of known accounts of the block
            if account in web3.eth.accounts:
                web3.geth.personal.unlock_account(account, '')
                # Calling the method to check current account role inside user contract
                real_role = self.get_user_role(account)
                # If the account isn't registered inside the contract
                if real_role == 0 and user_role != 0:
                    # The user is created with the given role inside the
                    web3.eth.default_account = account
                    self.user_contract.functions.createUser(
                        user_role).transact()
                else:
                    # The account is set as the default account
                    web3.eth.default_account = account
                return account
            # If the account isn't inside the current block's list of accounts
            else:
                # An error is raised
                raise Exception
        except Exception:
            raise Exception(
                "Error: it's impossible to verify your role and address, please try again")

    def get_user_role(self, address: ChecksumAddress = None) -> int:
        """
        Function used to validate user address and check if it corresponds to the given role. After
        validation function set the current user address as default web3 account in order to accomplish transactions
        Args:
            address: (Address): address of current logged user
        Returns:
            role: (int): role of current logged user
        """
        if address is None:
            return self.user_contract.functions.getRole().call()
        else:
            return self.user_contract.functions.getRole(address).call()

    def get_product(self, product_id: int) -> Product:
        """Gets the product from the blockchain with no information on raw materials and transformations.

        Args:
            product_id (`int`): the id of the product to get

        Returns:
            `Product`: a product from the blockchain
        """
        return Product.from_blockchain(
            self.user_contract.functions.getProductById(product_id).call()
        )

    # @singledispatch decorator allows function overloading depending on argument type
    # (in this case argument is a Product Object)
    # doc: https://docs.python.org/3/library/functools.html#functools.singledispatch
    @singledispatch
    def get_product_details(self, product: int) -> Product:
        """Gets information about raw material used and transformations performed on the specified product

        Args_
            product (`int`): the product id

        Returns
            `Product`: a product from the blockchain, with all the info
        """
        # The information regarding the raw materials used and the transformations implemented
        # are taken from the events emitted on the blockchain
        rm_events = self.event_logs.get_raw_materials_used_events(product)
        transformation_events = self.event_logs.get_transformations_events(product)

        # The Product object is taken form the blockchain and the materials and transformation info is added
        product = self.get_product(product)
        product.rawMaterials = [
            RawMaterial.from_event(event=ev) for ev in rm_events]
        product.transformations = [
            Transformation.from_event(event=ev) for ev in transformation_events
        ]
        return product

    @get_product_details.register
    def _(self, product: Product) -> Product:
        """Overload of the `get_product_details` function.
        Gets information about raw material used and transformations performed on the specified product.

        Args:
            product (`Product`): the product object without the requested info

        Returns:
            `Product`: a product from the blockchain, with all the info
        """
        # The info regarding the raw materials used and the transformations implemented
        # are taken from the events emitted on the blockchain
        rm_events = self.event_logs.get_raw_materials_used_events(product.product_id)
        transformation_events = self.event_logs.get_transformations_events(
            product.product_id)

        # materials and transformation info is added to the product
        product.rawMaterials = [
            RawMaterial.from_event(event=ev) for ev in rm_events]
        product.transformations = [
            Transformation.from_event(event=ev) for ev in transformation_events
        ]
        return product

    def get_all_raw_materials(self) -> List[RawMaterial]:
        """This function fetches and returns the list of all the raw materials saved on the blockchain

        Returns:
            `list[RawMaterial]`: a list of all the raw materials
        """
        return [
            RawMaterial.from_blockchain(rm)
            for rm in self.user_contract.functions.getRawMaterials().call()
        ]

    def get_usable_raw_materials(self, transformer_address) -> List[RawMaterial]:
        """This function fetches and returns a list of non-used raw materials that belong to the current user from the blockchain
        Args:
            transformer_address(`ChecksumAddress`): the address of the current user
        Returns:
            `list[RawMaterial]`: a list of all the non-used raw materials
        """
        rms = list(filter(lambda e: not e.is_used and e.transformer_address==transformer_address, self.get_all_raw_materials()))
        return rms

    def get_all_products(self) -> List[Product]:
        """
        Retrieves all `Product`s on the blockchain.
        This function returns a list of all the products without information
        about raw materials used or transformations.

        If you need information for a specific product, use
        `get_product_details`, or if you need them for all products use
        `get_all_products_detailed`


        Returns:
            `list[Product]`: a list of all the products on the blockchain
        """
        return [
            Product.from_blockchain(product)
            for product in self.user_contract.functions.getProducts().call()
        ]
