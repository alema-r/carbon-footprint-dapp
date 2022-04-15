import os
import sys
import io
import unittest
from off_chain.models import RawMaterial
import off_chain.connection as connection
import off_chain.controller_supplier as supplier
import off_chain.base_controller as controller
import unittest.mock

# TODO: testare overflow e underflow

class SupplierTest(unittest.TestCase):
    def setUp(self) -> None:
        #os.chdir(str(os.getcwd())+"/../")
        self.web3 = connection.connection(1)
        self.self.sup = supplier.self.supplier(web3=self.web3)
        self.self.sup.set_account_as_default(1, "0xca843569e3427144cead5e4d5999a3d0ccf92b8e")
        self.raw_material1 = RawMaterial("MateriaPrima11", 0, connection.web3.eth.default_account, 20)
        self.raw_material2 = RawMaterial("", 2, connection.web3.eth.default_account, 20)
        self.raw_material3 = RawMaterial("MateriaPrima12", 0, connection.web3.eth.default_account, 20)
        self.raw_material4 = RawMaterial("MateriaPrima13", 0, connection.web3.eth.default_account, 0)
        self.raw_material5 = RawMaterial("MateriaPrima14", 0, connection.web3.eth.default_account, 20)
        self.raw_material6 = RawMaterial("MateriaPrima15", 0, connection.web3.eth.default_account, 20)
        self.raw_material8 = RawMaterial("MateriaPrima16", 0, connection.web3.eth.default_account, 20)

    # Test to check a correctly added raw material
    def test_create_raw_materials(self):
        self.assertTrue(self.sup.create_raw_materials_on_blockchain([self.raw_material1, self.raw_material3]))
        self.assertIn(self.raw_material1, self.sup.get_all_raw_materials())
        self.assertIn(self.raw_material3, self.sup.get_all_raw_materials())
    
    # Misuse case test to check errore returned from Blockchain
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_misues1_creation_raw_material(self, mock_stdout):
        self.assertFalse(self.sup.create_raw_materials_on_blockchain([self.raw_material2]))
        self.assertEqual(mock_stdout.getvalue(), "execution reverted: One or more raw material has an empty name")
        self.assertNotIn(self.raw_material2, self.sup.get_all_raw_materials())

    
    # Misuse case test to check errore returned from Blockchain
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_misues2_creation_raw_material(self, mock_stdout):
        self.assertFalse(self.sup.create_raw_materials_on_blockchain([self.raw_material4]))
        self.assertEqual(mock_stdout.getvalue(),"execution reverted: One or more raw material has a carbon footprint value equal to 0")
        self.assertNotIn(self.raw_material4, self.sup.get_all_raw_materials())


    # Misuse case test to check errore returned from Blockchain
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_misues3_creation_raw_material(self, mock_stdout):
        self.assertFalse(self.sup.create_raw_materials_on_blockchain([self.raw_material5, self.raw_material6]))
        self.assertEqual(mock_stdout.getvalue(), "execution reverted: This lot of this raw material has been already inserted\n") 
        self.assertNotIn(self.raw_material5, self.sup.get_all_raw_materials())
        self.assertNotIn(self.raw_material6, self.sup.set_all_raw_materials())




if __name__ == '__main__':
    unittest.main()