"""
Module used to retrieve events on the blockchain
"""
from typing import List

from functools import partial
from web3.constants import ADDRESS_ZERO
from web3.datastructures import AttributeDict
import contracts


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
    """Retrieves all events about the termination of any product from the blockchain.

    Returns:
        List[AttributeDict]: a list of events
    """
    return finished_products_events().get_all_entries()


def get_minted_products_events() -> List[AttributeDict]:
    """Retrieves all events about the creation of any product from the blockchain.

    Returns:
        List[AttributeDict]: a list of events
    """
    return transfer_events(argument_filters={"from": ADDRESS_ZERO}).get_all_entries()


def get_transferred_products_events() -> List[AttributeDict]:
    """Retrieves all events about the transfer of any products from the blockchain

    Returns:
        List[AttributeDict]: a list of events
    """
    return list(
        filter(
            lambda e: e.args["from"] != ADDRESS_ZERO,
            transfer_events().get_all_entries(),
        )
    )


def get_raw_materials_used_events(product_id: int = None) -> List[AttributeDict]:
    """Retrieves all events related to the use of any raw material from the blockchain.

    Args:
        product_id (int, optional): If specified, retrieves all raw materials used for this
        particular product. Defaults to None.

    Returns:
        List[AttributeDict]: a list of events
    """
    if product_id is not None:
        return list(
            filter(
                lambda e: e.args.pId == product_id,
                raw_materials_used_events().get_all_entries(),
            )
        )
    return raw_materials_used_events().get_all_entries()


def get_transformations_events(product_id: int = None) -> List[AttributeDict]:
    """Retrieves all events related to any transformation from the blockchain.

    Args:
        product_id (int, optional): If specified, retrieves all transformations performed
        on this particular product. Defaults to None.

    Returns:
        List[AttributeDict]: a list of events
    """
    if product_id is not None:
        return list(
            filter(
                lambda e: e.args.pId == product_id,
                transformation_events().get_all_entries(),
            )
        )
    return transformation_events().get_all_entries()
