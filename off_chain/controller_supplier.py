from web3 import Web3

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
            raw_material_transformers_list = [
                raw_material.transformer_address for raw_material in raw_materials]
            self.user_contract.functions.createRawMaterials(raw_materials_name_list, raw_materials_lot_list,
                                                            raw_materials_cf_list, raw_material_transformers_list).transact()
            return True

        except Exception as e:
            # These are custom exceptions
            if (str(e) == "No raw material names were provided. Insertion failed") or (
                    str(e) == "No raw material lots provided. Insertion failed") or (
                    str(e) == "No raw material carbon footprint provided. Insertion failed") or (
                    str(e) == "No transformer provided. Insertion failed") or (
                    str(e) == "The number of raw materials doesn't match the number of lots. Insertion failed.") or (
                    str(e) == "The number of raw materials doesn't match the number of carbon footprints. Insertion failed.") or (
                    str(e) == "Raw material's number doesn't match the number of transformers. Insertion failed."):
                print(e)
            # And these are other generic exceptions
            else:
                print(
                    "Insertion of raw materials failed. Please insert raw materials again")
            return False
