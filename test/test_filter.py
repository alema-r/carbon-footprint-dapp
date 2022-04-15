import operator
import os
import unittest

from hexbytes import HexBytes

from off_chain.blockchain import set_account_as_default
import off_chain.connection as connection
import off_chain.contracts as contracts
from off_chain.filter import simple_filter, and_filter, or_filter, personalized_contains
from off_chain.models import Product


def get_products():
    return [Product(1, 'Prodotto1', '0x0fbdc686b912d7722dc86510934589e0aaf3b55a', 45, True),
            Product(2, 'Prodotto2', '0x30Fd3731FE1Deee29f9325c19e22C2A71099240b', 70, True),
            Product(3, 'Product1', '0x30Fd3731FE1Deee29f9325c19e22C2A71099240b', 45, False),
            Product(4, 'Prodotto3', '0x0fbdc686b912d7722dc86510934589e0aaf3b55a', 68, True),
            Product(5, 'Product2', '0x30Fd3731FE1Deee29f9325c19e22C2A71099240b', 48, False),
            Product(6, 'Nome', '0x0fbdc686b912d7722dc86510934589e0aaf3b55a', 60, False)]


def get_events():
    return [{'args': {'transformer': '0x30Fd3731FE1Deee29f9325c19e22C2A71099240b', 'supplier': '0x788809a43373249aAC1938A19F66218cf590A5c6', 'pId': 1, 'name': 'MateriaPrima', 'lot': 0, 'cf': 10}, 'event': 'rawMaterialIsUsed', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xc223b643654a45e196b51a3461b07fbdd650eb96bab640d9caa71c3b1d563ae3'), 'address': '0x6a55e9Af01d3741079C1b855857933F5e2fa3D5a', 'blockHash': HexBytes('0x1349ca0c238612f43ccd8692763206a5853ee6c8816c2ce2d4dc4969ef398a58'), 'blockNumber': 132},
            {'args': {'transformer': '0x0fbdc686b912d7722dc86510934589e0aaf3b55a', 'supplier': '0xca843569e3427144cead5e4d5999a3d0ccf92b8e', 'pId': 1, 'name': 'RawMaterial', 'lot': 2, 'cf': 15}, 'event': 'rawMaterialIsUsed',  'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xc223b643654a45e196b51a3461b07fbdd650eb96bab640d9caa71c3b1d563ae3'), 'address': '0x6a55e9Af01d3741079C1b855857933F5e2fa3D5a', 'blockHash': HexBytes('0x1349ca0c238612f43ccd8692763206a5853ee6c8816c2ce2d4dc4969ef398a58'), 'blockNumber': 132},
            {'args': {'transformer': '0x0fbdc686b912d7722dc86510934589e0aaf3b55a', 'supplier': '0xca843569e3427144cead5e4d5999a3d0ccf92b8e', 'pId': 2, 'name': 'RawMaterial', 'lot': 0, 'cf': 20}, 'event': 'rawMaterialIsUsed', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xc223b643654a45e196b51a3461b07fbdd650eb96bab640d9caa71c3b1d563ae3'), 'address': '0x6a55e9Af01d3741079C1b855857933F5e2fa3D5a', 'blockHash': HexBytes('0x1349ca0c238612f43ccd8692763206a5853ee6c8816c2ce2d4dc4969ef398a58'), 'blockNumber': 132},
            {'args': {'transformer': '0x30Fd3731FE1Deee29f9325c19e22C2A71099240b', 'supplier': '0x788809a43373249aAC1938A19F66218cf590A5c6', 'pId': 2, 'name': 'NomeRM', 'lot': 0, 'cf': 30}, 'event': 'rawMaterialIsUsed', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xc223b643654a45e196b51a3461b07fbdd650eb96bab640d9caa71c3b1d563ae3'), 'address': '0x6a55e9Af01d3741079C1b855857933F5e2fa3D5a', 'blockHash': HexBytes('0x1349ca0c238612f43ccd8692763206a5853ee6c8816c2ce2d4dc4969ef398a58'), 'blockNumber': 132},
            {'args': {'transformer': '0x0fbdc686b912d7722dc86510934589e0aaf3b55a', 'supplier': '0xca843569e3427144cead5e4d5999a3d0ccf92b8e', 'pId': 3, 'name': 'RawMaterial', 'lot': 1, 'cf': 25}, 'event': 'rawMaterialIsUsed', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xc223b643654a45e196b51a3461b07fbdd650eb96bab640d9caa71c3b1d563ae3'), 'address': '0x6a55e9Af01d3741079C1b855857933F5e2fa3D5a', 'blockHash': HexBytes('0x1349ca0c238612f43ccd8692763206a5853ee6c8816c2ce2d4dc4969ef398a58'), 'blockNumber': 132},
            {'args': {'transformer': '0x30Fd3731FE1Deee29f9325c19e22C2A71099240b', 'supplier': '0x788809a43373249aAC1938A19F66218cf590A5c6', 'pId': 4, 'name': 'MateriaPrima', 'lot': 1, 'cf': 35}, 'event': 'rawMaterialIsUsed', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xc223b643654a45e196b51a3461b07fbdd650eb96bab640d9caa71c3b1d563ae3'), 'address': '0x6a55e9Af01d3741079C1b855857933F5e2fa3D5a', 'blockHash': HexBytes('0x1349ca0c238612f43ccd8692763206a5853ee6c8816c2ce2d4dc4969ef398a58'), 'blockNumber': 132},
            {'args': {'transformer': '0x0fbdc686b912d7722dc86510934589e0aaf3b55a', 'supplier': '0xca843569e3427144cead5e4d5999a3d0ccf92b8e', 'pId': 4, 'name': 'Nome', 'lot': 0, 'cf': 13}, 'event': 'rawMaterialIsUsed', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xc223b643654a45e196b51a3461b07fbdd650eb96bab640d9caa71c3b1d563ae3'), 'address': '0x6a55e9Af01d3741079C1b855857933F5e2fa3D5a', 'blockHash': HexBytes('0x1349ca0c238612f43ccd8692763206a5853ee6c8816c2ce2d4dc4969ef398a58'), 'blockNumber': 132},
            {'args': {'transformer': '0x0fbdc686b912d7722dc86510934589e0aaf3b55a', 'supplier': '0x788809a43373249aAC1938A19F66218cf590A5c6', 'pId': 5, 'name': 'ProvaMateria', 'lot': 0, 'cf': 28}, 'event': 'rawMaterialIsUsed', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xc223b643654a45e196b51a3461b07fbdd650eb96bab640d9caa71c3b1d563ae3'), 'address': '0x6a55e9Af01d3741079C1b855857933F5e2fa3D5a', 'blockHash': HexBytes('0x1349ca0c238612f43ccd8692763206a5853ee6c8816c2ce2d4dc4969ef398a58'), 'blockNumber': 132},
            {'args': {'transformer': '0x30Fd3731FE1Deee29f9325c19e22C2A71099240b', 'supplier': '0x788809a43373249aAC1938A19F66218cf590A5c6', 'pId': 6, 'name': 'ProvaMateria', 'lot': 1, 'cf': 45}, 'event': 'rawMaterialIsUsed', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xc223b643654a45e196b51a3461b07fbdd650eb96bab640d9caa71c3b1d563ae3'), 'address': '0x6a55e9Af01d3741079C1b855857933F5e2fa3D5a', 'blockHash': HexBytes('0x1349ca0c238612f43ccd8692763206a5853ee6c8816c2ce2d4dc4969ef398a58'), 'blockNumber': 132},
            {'args': {'transformer': '0x0fbdc686b912d7722dc86510934589e0aaf3b55a', 'supplier': '0x788809a43373249aAC1938A19F66218cf590A5c6', 'pId': 6, 'name': 'ProvaMateria', 'lot': 2, 'cf': 40}, 'event': 'rawMaterialIsUsed', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0xc223b643654a45e196b51a3461b07fbdd650eb96bab640d9caa71c3b1d563ae3'), 'address': '0x6a55e9Af01d3741079C1b855857933F5e2fa3D5a', 'blockHash': HexBytes('0x1349ca0c238612f43ccd8692763206a5853ee6c8816c2ce2d4dc4969ef398a58'), 'blockNumber': 132}]


class FilterTest(unittest.TestCase):

    def test_name_filter(self):
        criteria = {"elements": get_products, "value": 'uct', "field": "name", "operator": personalized_contains, "event": False}
        expected = [3, 5]
        self.assertListEqual(expected, simple_filter([], criteria))

    def test_owner_filter(self):
        criteria = {"elements": get_products, "value": '0x0fbdc686b912d7722dc86510934589e0aaf3b55a', "field": "address", "operator": operator.eq, "event": False}
        expected = [1, 4, 6]
        self.assertListEqual(expected, simple_filter([], criteria))

    def test_cf_filter(self):
        criteria = {"elements": get_products, "value": 50, "field": "cf", "operator": operator.le, "event": False}
        expected = [1, 3, 5]
        self.assertListEqual(expected, simple_filter([], criteria))

    def test_ended_filter(self):
        criteria = {"elements": get_products, "value": False, "field": "is_ended", "operator": operator.eq, "event": False}
        expected = [3, 5, 6]
        self.assertListEqual(expected, simple_filter([], criteria))

    def test_supplier_filter(self):
        criteria = {"elements": get_events, "value": '0xca843569e3427144cead5e4d5999a3d0ccf92b8e', "field": "supplier", "operator": operator.eq, "event": True}
        expected = [1, 2, 3, 4]
        self.assertListEqual(expected, simple_filter([], criteria))

    def test_transformer_filter(self):
        criteria = {"elements": get_events, "value": '0x30Fd3731FE1Deee29f9325c19e22C2A71099240b', "field": "transformer", "operator": operator.eq, "event": True}
        expected = [1, 2, 4, 6]
        self.assertListEqual(expected, simple_filter([], criteria))

    def test_rm_name_filter(self):
        criteria = {"elements": get_events, "value": 'ome', "field": "name", "operator": personalized_contains, "event": True}
        expected = [2, 4]
        self.assertListEqual(expected, simple_filter([], criteria))

    def test_and_filter(self):
        criteria = [{"elements": get_events, "value": 'ome', "field": "name", "operator": personalized_contains, "event": True},
                    {"elements": get_products, "value": '0x0fbdc686b912d7722dc86510934589e0aaf3b55a', "field": "address", "operator": operator.eq, "event": False}]
        expected = [4]
        result = simple_filter([], criteria[0])
        self.assertListEqual(expected, and_filter(result, criteria[1]))

    def test_or_filter(self):
        criteria = [{"elements": get_products, "value": 'uct', "field": "name", "operator": personalized_contains, "event": False},
                    {"elements": get_events, "value": '0xca843569e3427144cead5e4d5999a3d0ccf92b8e', "field": "supplier", "operator": operator.eq, "event": True}]
        expected = [1, 2, 3, 4, 5]
        result = simple_filter([], criteria[0])
        self.assertListEqual(expected, or_filter(result, criteria[1]))


if __name__ == '__main__':
    unittest.main()
