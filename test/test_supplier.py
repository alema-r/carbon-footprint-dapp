import os
import sys
import io
import unittest

from web3 import Web3
from off_chain.models import RawMaterial
import off_chain.connection as connection
import off_chain.controller_supplier as supplier
import off_chain.base_controller as controller
import unittest.mock

class SupplierTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(str(os.getcwd())+"/../")
        cls.web3 = connection.connection(1)
        cls.sup = supplier.Supplier(web3=cls.web3)
        cls.transformer_address = Web3.toChecksumAddress("0x0fbdc686b912d7722dc86510934589e0aaf3b55a")
        cls.sup.set_account_as_default(user_role = 1, address="0xca843569e3427144cead5e4d5999a3d0ccf92b8e")
        cls.client_address = Web3.toChecksumAddress("0xed9d02e382b34818e88b88a309c7fe71e65f419d")
        cls.raw_materials_list = []

        for i in range(30, 43):
            nome = f"MateriaPrimaTest{i}"
            lotto = int(i // 4)
            sup = cls.web3.eth.default_account
            cf = (i // 4)*100 + (i % 4)*10 + 10
            tr = cls.transformer_address
            cls.raw_materials_list.append(RawMaterial(nome, lotto, sup, cf, transformer_address = tr))


        cls.raw_material1 = RawMaterial("MateriaPrima11", 0, cls.web3.eth.default_account, 20, transformer_address= cls.transformer_address)
        cls.raw_material2 = RawMaterial("", 2, cls.web3.eth.default_account, 20, transformer_address=cls.transformer_address)
        cls.raw_material3 = RawMaterial("MateriaPrima12", 0, cls.web3.eth.default_account, 20, transformer_address= cls.client_address)
        cls.raw_material4 = RawMaterial("MateriaPrima13", 0, cls.web3.eth.default_account, 0, transformer_address=cls.transformer_address)
        cls.raw_material5 = RawMaterial("MateriaPrima15", 0, cls.web3.eth.default_account, 20, transformer_address=cls.transformer_address)
        cls.raw_material6 = RawMaterial("MateriaPrima15", 0, cls.web3.eth.default_account, 20, transformer_address=cls.transformer_address)
        cls.raw_material8 = RawMaterial("MateriaPrima16", 0, cls.web3.eth.default_account, 20, transformer_address=cls.transformer_address)
        cls.raw_material9 = RawMaterial("Materiaprima17", 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999, cls.web3.eth.default_account, 20, transformer_address=cls.transformer_address )
        cls.raw_materials_list.append(cls.raw_material1)

    # Test to check a correctly added raw material
    def test_create_raw_materials(self):
        self.assertTrue(self.sup.create_raw_materials_on_blockchain(self.raw_materials_list))
        for raw_material in self.raw_materials_list:
            self.assertIn(raw_material , self.sup.get_all_raw_materials())
    
    
    # Misuse case test to check errore returned from Blockchain
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_misues1_creation_raw_material(self, mock_stdout):
        self.assertFalse(self.sup.create_raw_materials_on_blockchain([self.raw_material2]))
        self.assertEqual(mock_stdout.getvalue(), "execution reverted: One or more raw material has an empty name\n")
        self.assertNotIn(self.raw_material2, self.sup.get_all_raw_materials())
    

    
    # Misuse case test to check errore returned from Blockchain
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_misues2_creation_raw_material(self, mock_stdout):
        self.assertFalse(self.sup.create_raw_materials_on_blockchain([self.raw_material4]))
        self.assertEqual(mock_stdout.getvalue(),"execution reverted: One or more raw material has a carbon footprint value equal to 0\n")
        self.assertNotIn(self.raw_material4, self.sup.get_all_raw_materials())


    # Misuse case test to check errore returned from Blockchain
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_misues3_creation_raw_material(self, mock_stdout):
        self.assertFalse(self.sup.create_raw_materials_on_blockchain([self.raw_material5, self.raw_material6]))
        self.assertEqual(mock_stdout.getvalue(), "execution reverted: This lot of this raw material has been already inserted. Insertion failed.\n") 
        self.assertNotIn(self.raw_material5, self.sup.get_all_raw_materials())
        self.assertNotIn(self.raw_material6, self.sup.get_all_raw_materials())
        
        
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_misuse4_creation_raw_material(self, mock_stdout):
        self.assertFalse(self.sup.create_raw_materials_on_blockchain([self.raw_material3]))
        self.assertEqual(mock_stdout.getvalue(), "execution reverted: One or more inserted addresses are not transformer addresses\n") 
        self.assertNotIn(self.raw_material3, self.sup.get_all_raw_materials())


    # Testing for overflow
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_overflow_creation_raw_material(self, mock_stdout):
        self.assertFalse(self.sup.create_raw_materials_on_blockchain([self.raw_material9]))
        self.assertEqual(mock_stdout.getvalue(), "Insertion of raw materials failed. Please insert raw materials again\n") 
        self.assertNotIn(self.raw_material9, self.sup.get_all_raw_materials())





if __name__ == '__main__':
    unittest.main()