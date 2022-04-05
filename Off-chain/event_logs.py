"""
Module used to retrieve events on the blockchain
"""
from typing import List

import contracts
from functools import partial
from web3.constants import ADDRESS_ZERO
from web3.datastructures import AttributeDict


transformation_events = partial(
    contracts.cf_contract.events.newCFAdded().createFilter, fromBlock=0x0
)
raw_materials_used_events = partial(
    contracts.cf_contract.events.rawMaterialIsUsed().createFilter, fromBlock=0x0
)
finished_products_events = partial(
    contracts.cf_contract.events.productIsFinished().createFilter, fromBlock=0x0
)
new_raw_material_lot_added_events_filter = partial(
    contracts.cf_contract.events.newRawMaterialLotAdded().createFilter, fromBlock=0x0
)
transfer_events = partial(
    contracts.cf_contract.events.Transfer().createFilter, fromBlock=0x0
)

def get_finished_products_events() -> List[AttributeDict]:
    return finished_products_events().get_all_entries()

def get_minted_products_events() -> List[AttributeDict]:
    return transfer_events(
        argument_filters={"from": ADDRESS_ZERO}
    ).get_all_entries()

def get_transferred_products_events() -> List[AttributeDict]:
    return list(
        filter(
            lambda e: e.args["from"] != ADDRESS_ZERO,
            transfer_events().get_all_entries(),
        )
    )

def get_raw_materials_used_events(product_id: int=None) -> List[AttributeDict]:
    if product_id is not None:
        return list(
            filter(
                lambda e: e.args.pId == product_id,
                raw_materials_used_events().get_all_entries(),
            )
        )
    return raw_materials_used_events().get_all_entries()


def get_transformations_events(product_id: int=None) -> List[AttributeDict]:
    if product_id is not None:
        return list(
            filter(
                lambda e: e.args.pId == product_id,
                transformation_events().get_all_entries(),
            )
        )
    return transformation_events().get_all_entries()
