import unittest

import inquirer
import inquirer.errors
import off_chain.validation as validation


class ValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.correct_supplier_address = "0xca843569e3427144cead5e4d5999a3d0ccf92b8e"
        cls.correct_transformer_address = "0x0fbdc686b912d7722dc86510934589e0aaf3b55a"
        cls.client_address = "0xf62aa436fc524e574bfeba5b6ad8159bcff407a5"
        cls.incorrect_address = "indirizzoovviamenteerrato"
        cls.valid_cf = 100
        cls.invalid_cf = 10-20
        cls.invalid_cf1 = "-10"
        cls.invalid_cf2 = "prova"
        cls.invalid_cf3 = 0
        cls.invalid_cf4 = 1000001
        cls.valid_lot = 1
        cls.invalid_lot = 10-20
        cls.invalid_lot1 = "-10"
        cls.invalid_lot2 = "prova"
        cls.invalid_lot3 = "   "
        cls.invalid_lot4 = 1000001
        cls.valid_id = 1
        cls.invalid_id = 10-20
        cls.invalid_id1 = "-10"
        cls.invalid_id2 = "prova"
        cls.invalid_id3 = "   "
        cls.valid_name = "prova 1 2"
        cls.invalid_name = "/prova"
        cls.invalid_name1 = " "
        cls.invalid_name2 ="a      "
        cls.invalid_name3 = "a"
        cls.invalid_name4 = "provaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" 
        cls.invalid_name5 = "prova_1"
    
    def test_supplier_address_validation(self):
        self.assertTrue(validation.address_validation(dict(), "0xca843569e3427144cead5e4d5999a3d0ccf92b8e"))
        with self.assertRaises(inquirer.errors.ValidationError):
            validation.address_validation(dict(), self.incorrect_address)


    def test_transformer_address_validation(self):
        self.assertTrue(validation.address_validation(dict(), "0x0fbdc686b912d7722dc86510934589e0aaf3b55a"))
        with self.assertRaises(inquirer.errors.ValidationError):
            validation.address_validation(dict(), self.incorrect_address)

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