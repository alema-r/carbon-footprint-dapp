import unittest

import inquirer
import inquirer.errors
import off_chain.validation as validation
import off_chain.connection as connection
import off_chain.contracts as contracts
import off_chain.blockchain as blockchain


class ValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        connection.connection(1)
        contracts.building_contracts()
        blockchain.set_account_as_default(1, "0xca843569e3427144cead5e4d5999a3d0ccf92b8e")
        self.correct_supplier_address = "0xca843569e3427144cead5e4d5999a3d0ccf92b8e"
        self.correct_transformer_address = "0x0fbdc686b912d7722dc86510934589e0aaf3b55a"
        self.client_address = "0xf62aa436fc524e574bfeba5b6ad8159bcff407a5"
        self.incorrect_address = "indirizzoovviamenteerrato"
        self.valid_cf = 100
        self.invalid_cf = 10-20
        self.invalid_cf1 = "-10"
        self.invalid_cf2 = "prova"
        self.invalid_cf3 = 0
        self.valid_lot = 1
        self.invalid_lot = 10-20
        self.invalid_lot1 = "-10"
        self.invalid_lot2 = "prova"
        self.invalido_lot3 = "   "
        self.valid_id = 1
        self.invalid_id = 10-20
        self.invalid_id1 = "-10"
        self.invalid_id2 = "prova"
        self.invalid_id3 = "   "
        self.valid_name = "prova 1 2"
        self.invalid_name = "/prova"
        self.invalid_name1 = " "
        self.invalid_name2 ="a      "
        self.invalid_name3 = "a"
        self.invalid_name4 = "provaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" 
        self.invalid_name5 = "prova_1"
    
    def test_supplier_address_validation(self):
        self.assertTrue(validation.supplier_address_validation(dict(), "0xca843569e3427144cead5e4d5999a3d0ccf92b8e"))
        with self.assertRaises(inquirer.errors.ValidationError):
            validation.supplier_address_validation(dict(), self.incorrect_address)
            validation.supplier_address_validation(dict(), self.client_address)


    def test_transformer_address_validation(self):
        self.assertTrue(validation.transformer_address_validation(dict(), "0x0fbdc686b912d7722dc86510934589e0aaf3b55a"))
        with self.assertRaises(inquirer.errors.ValidationError):
            validation.supplier_address_validation(dict(), self.incorrect_address)
            validation.supplier_address_validation(dict(), self.client_address)

    def test_carbon_fp_input_validation(self):
        self.assertTrue(validation.carbon_fp_input_validation(dict(), str(self.valid_cf)))
        with self.assertRaises(inquirer.errors.ValidationError):
            validation.carbon_fp_input_validation(dict(), str(self.invalid_cf))
            validation.carbon_fp_input_validation(dict(), str(self.invalid_cf1))
            validation.carbon_fp_input_validation(dict(), str(self.invalid_cf2))
            validation.carbon_fp_input_validation(dict(), str(self.invalid_cf3))

    def test_lot_input_validation(self):
        with self.assertRaises(inquirer.errors.ValidationError):
            validation.lot_input_validation(dict(), str(self.valid_lot))
            validation.carbon_fp_input_validation(dict(), str(self.invalid_lot))
            validation.carbon_fp_input_validation(dict(), str(self.invalid_lot1))
            validation.carbon_fp_input_validation(dict(), str(self.invalid_lot2))
            validation.carbon_fp_input_validation(dict(), str(self.invalid_lot3))

    def test_id_input_validation(self):
        self.assertTrue(validation.id_input_validation(dict(), str(self.valid_id)))
        with self.assertRaises(inquirer.errors.ValidationError):
            validation.id_input_validation(dict(), str(self.invalid_id))
            validation.id_input_validation(dict(), str(self.invalid_id1))
            validation.id_input_validation(dict(), str(self.invalid_id2))
            validation.id_input_validation(dict(), str(self.invalid_id3))

    def test_name_input_validation(self):
        self.assertTrue(validation.name_input_validation(dict(), str(self.valid_name)))
        with self.assertRaises(inquirer.errors.ValidationError):
            validation.name_input_validation(dict(), str(self.invalid_name))
            validation.name_input_validation(dict(), str(self.invalid_name1))
            validation.name_input_validation(dict(), str(self.invalid_name2))
            validation.name_input_validation(dict(), str(self.invalid_name3))
            validation.name_input_validation(dict(), str(self.invalid_name4))
            validation.name_input_validation(dict(), str(self.invalid_name5))
    



if __name__ == '__main__':
    unittest.main()