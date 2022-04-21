from typing import List

from eth_typing import ChecksumAddress
from web3 import Web3, exceptions

from off_chain.base_controller import BlockChain


class Transformer(BlockChain):
    def __init__(self, web3: Web3):
        super().__init__(web3)

    def get_updatable_user_products(self, user_address: ChecksumAddress):
        """This function filters the products stored in the blockhain. It returns a list of the products that are owned by the
        current user.

        Args:
            user_address (`ChecksumAddress`): the address of the current user

        Returns:
            `list[Product]`: the list of the products owned by the current user
        """
        all_products = self.get_all_products()
        return list(filter(lambda p: (p.address == user_address and not p.is_ended), all_products))

    def add_transformation_on_blockchain(self, carb_foot: int, product_id: int, is_the_final: bool) -> bool:
        """This function connects to the blockchain to add a new transformation

        Args:
            carb_foot (int): the value of the carbon footprint
            product_id (int): the id of the product to which a new transformation needs to be added
            is_the_final (bool): boolean that indicates if this is the final transformation of the production chain
        """
        try:
            tx_hash = self.user_contract.functions.addTransformation(
                carb_foot, product_id, is_the_final).transact()
            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return True

        except exceptions.ContractLogicError as e:
            print(e)
            return False
        
        except Exception as e:
            print("Insertion of transformation failed. Please try again")
            return False

    def transfer_product_on_blockchain(self, transfer_to: ChecksumAddress, product_id: int):
        """This function connects to the blockchain to transfer the ownership of a product

        Args:
            transfer_to (ChecksumAddress): the address of the user to whom the product ownership needs to be transferred
            product_id (int): the id of the product to transfer

        Raises:
            `Exception`: if the operations fails
        """
        try:
            tx_hash = self.user_contract.functions.transferCP(
                transfer_to, product_id).transact()
            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return True
        
        except exceptions.ContractLogicError as e:
            print(e)
            return False
        
        except Exception as e:
            print("Transfer failed. Please try again")
            return False
    

    def create_new_product_on_blockchain(self, product_name: str, raw_material_ids: List[int]):
        """This function connects to the blockchain to add a new product

        Args:
            product_name (str): the name of the product to create
            raw_material_ids (list[int]): Ids of the raw materials to use for the product

        Raises:
            Exception: if the operations fails
        """
        try:
            tx_hash = self.user_contract.functions.createProduct(
                product_name, raw_material_ids).transact()
            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return True
        
        except exceptions.ContractLogicError as e:
            print(e)
            return False
        
        except Exception as e:
            print("Creation failed. Please try again.")
            return False
        
