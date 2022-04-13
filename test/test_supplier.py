import os
import unittest
from off_chain.models import RawMaterial
import off_chain.connection as connection
import off_chain.contracts as contracts
from off_chain.blockchain import create_raw_materials_on_blockchain, get_all_raw_materials, set_account_as_default


class SupplierTest(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir(str(os.getcwd())+"/../")
        connection.connection(1)
        contracts.building_contracts()
        set_account_as_default(1, "0xca843569e3427144cead5e4d5999a3d0ccf92b8e")
        self.raw_material = RawMaterial("MateriaPrima5", 0, connection.web3.eth.default_account, 20)

    def test_create_raw_materials(self):
        self.assertTrue(create_raw_materials_on_blockchain([self.raw_material]))
        self.assertIn(self.raw_material, get_all_raw_materials())


if __name__ == '__main__':
    unittest.main()
