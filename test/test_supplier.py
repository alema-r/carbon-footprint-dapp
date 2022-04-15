import os
import sys
import io
import unittest
from off_chain.models import RawMaterial
import off_chain.connection as connection
import off_chain.contracts as contracts
from off_chain.blockchain import create_raw_materials_on_blockchain, get_all_raw_materials, set_account_as_default
import unittest.mock
import web3

# TODO: testare overflow e underflow

class SupplierTest(unittest.TestCase):
    def setUp(self) -> None:
        #os.chdir(str(os.getcwd())+"/../")
        connection.connection(1)
        contracts.building_contracts()
        set_account_as_default(1, "0xca843569e3427144cead5e4d5999a3d0ccf92b8e")
        self.raw_material1 = RawMaterial("MateriaPrima140", 0, connection.web3.eth.default_account, 20)
        self.raw_material2 = RawMaterial("", 2, connection.web3.eth.default_account, 20)
        self.raw_material3 = RawMaterial("MateriaPrima180", 0, connection.web3.eth.default_account, 20)
        self.raw_material4 = RawMaterial("MateriaPrima8", 0, connection.web3.eth.default_account, 0)
        self.raw_material5 = RawMaterial("MateriaPrima10", 0, connection.web3.eth.default_account, 20)
        self.raw_material6 = RawMaterial("MateriaPrima10", 0, connection.web3.eth.default_account, 20)
        self.raw_material8 = RawMaterial("MateriaPrima21", 0, connection.web3.eth.default_account, 20)

    # Test to check a correctly added raw material
    def test_create_raw_materials(self):
        self.assertTrue(create_raw_materials_on_blockchain([self.raw_material1, self.raw_material3]))
        self.assertIn(self.raw_material1, get_all_raw_materials())
        self.assertIn(self.raw_material3, get_all_raw_materials())
    
    # Misuse case test to check errore returned from Blockchain
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_misues1_creation_raw_material(self, mock_stdout):
        self.assertFalse(create_raw_materials_on_blockchain([self.raw_material2]))
        self.assertEqual(mock_stdout.getvalue(), "execution reverted: One or more raw material has an empty name")
        self.assertNotIn(self.raw_material2, get_all_raw_materials())

    
    # Misuse case test to check errore returned from Blockchain
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_misues2_creation_raw_material(self, mock_stdout):
        self.assertFalse(create_raw_materials_on_blockchain([self.raw_material4]))
        self.assertEqual(mock_stdout.getvalue(),"execution reverted: One or more raw material has a carbon footprint value equal to 0")
        self.assertNotIn(self.raw_material4, get_all_raw_materials())


    #TODO: testare questa funzione dopo aver capito come cambia il programma
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_misues2_creation_raw_material(self, mock_stdout):
        self.assertFalse(create_raw_materials_on_blockchain([self.raw_material8]))
        self.assertEqual(mock_stdout.getvalue(),"execution reverted: One or more raw material has a carbon footprint value equal to 0")
        self.assertNotIn(self.raw_material8, get_all_raw_materials())
        

    # Misuse case test to check errore returned from Blockchain
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_misues3_creation_raw_material(self, mock_stdout):
        self.assertFalse(create_raw_materials_on_blockchain([self.raw_material5, self.raw_material6]))
        self.assertEqual(mock_stdout.getvalue(), "execution reverted: This lot of this raw material has been already inserted\n") 
        self.assertNotIn(self.raw_material5, get_all_raw_materials())
        self.assertNotIn(self.raw_material6, get_all_raw_materials())




if __name__ == '__main__':
    unittest.main()
