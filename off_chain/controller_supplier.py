from web3 import exceptions, Web3

from off_chain.base_controller import BlockChain


class Supplier(BlockChain):
    def __init__(self, web3: Web3):
        super().__init__(web3)

    def create_raw_materials_on_blockchain(self, raw_materials) -> bool:
        """Functions that inserts a new raw materials on the blockchain

        Args:
            raw_materials (`list[RawMaterial]`): List of raw materials that must be inserted
        """
        try:
            raw_materials_name_list = [
                raw_material.name for raw_material in raw_materials]
            raw_materials_lot_list = [
                raw_material.lot for raw_material in raw_materials]
            raw_materials_cf_list = [
                raw_material.cf for raw_material in raw_materials]
            self.user_contract.functions.createRawMaterials(raw_materials_name_list, raw_materials_lot_list,
                                                            raw_materials_cf_list).transact()
            return True

        except exceptions as e:
            # These are custom exceptions
            if (str(e) == "execution reverted: No raw material names were provided. Insertion Failed") or (
                    str(e) == "execution reverted: No raw material lots provided. Insertion Failed") or (
                    str(e) == "execution reverted: No raw material carbon footprint provided. Insertion Failed") or (
                    str(e) == "execution reverted: Raw material's number doesn't match lot's number") or (
                    str(e) == "execution reverted: Raw material's number doesn't match carbon footprint's number") or (
                    str(e) == "execution reverted: One or more raw material has an empty name") or (
                    str(e) == "execution reverted: One or more raw material has a carbon footprint value equal to 0" ) or (
                    str(e) == "execution reverted: This lot of this raw material has been already inserted"):
                print(e)
            # And these are other generic exceptions
            else:
                print("Insertion of raw materials failed. Please insert raw materials again")
            return False
