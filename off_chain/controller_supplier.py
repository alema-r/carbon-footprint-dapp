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
            rm_name_list = []
            rm_lot_list = []
            rm_cf_list = []
            rm_tr_list = []
            for raw_mat in raw_materials:
                rm_name_list.append(raw_mat.name)
                rm_lot_list.append(raw_mat.lot)
                rm_cf_list.append(raw_mat.cf)
                rm_tr_list.append(raw_mat.transformer_address)
            
            self.user_contract.functions.createRawMaterials(
                rm_name_list,
                rm_lot_list,
                rm_cf_list,
                rm_tr_list,
            ).transact()
            return True
            
        except exceptions.ContractLogicError as e:
            print(e)
            return False

        except Exception:
            print("Insertion of raw materials failed. Please insert raw materials again")
            return False

        '''
        except Exception as e:
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
                print(
                    "Insertion of raw materials failed. Please insert raw materials again")
        '''