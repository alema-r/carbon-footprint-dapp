import io
import unittest
import unittest.mock

from off_chain import connection
from off_chain.controller_transformer import Transformer
from off_chain.models import Product


class TransformerTest(unittest.TestCase):

    web3 = None
    transformer_controller = None
    transformer = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.web3 = connection.connection(2)
        cls.transformer_controller = Transformer(cls.web3)
        if len(cls.web3.geth.personal.list_accounts()) < 2:
            cls.transformer = cls.web3.geth.personal.new_account("")
            cls.web3.geth.personal.unlock_account(cls.transformer, "")
            cls.web3.eth.default_account = cls.transformer
            tx_hash = cls.transformer_controller.user_contract.functions.createUser(
                2
            ).transact()
            cls.web3.eth.wait_for_transaction_receipt(tx_hash)
        else:
            cls.transformer = cls.web3.geth.personal.list_accounts()[0]
        cls.web3.geth.personal.unlock_account(cls.transformer, "")
        cls.transformer_controller.set_account_as_default(
            2, "0x0fbdc686b912d7722dc86510934589e0aaf3b55a"
        )
        address = cls.web3.eth.default_account
        raw_materials = cls.transformer_controller.get_all_raw_materials()
        product_cf_1 = sum(
            [
                raw_material.cf
                for raw_material in raw_materials
                if raw_material.material_id in [0, 2]
            ]
        )
        product_cf_2 = sum(
            [
                raw_material.cf
                for raw_material in raw_materials
                if raw_material.material_id in [4, 6]
            ]
        )
        product_cf_3 = sum(
            [
                raw_material.cf
                for raw_material in raw_materials
                if raw_material.material_id in [5, 9]
            ]
        )
        product_cf_4 = sum(
            [
                raw_material.cf
                for raw_material in raw_materials
                if raw_material.material_id in [1, 7]
            ]
        )
        cls.product_1 = Product("Prodotto1 Test", address, product_cf_1, product_id=1)
        cls.product_2 = Product("Prodotto2 Test", address, product_cf_2, product_id=2)
        cls.product_3 = Product("Prodotto3 Test", address, product_cf_2, product_id=3)
        cls.product_4 = Product("", address, product_cf_3)
        cls.product_5 = Product("Prodotto Misuse", address, product_cf_4)

    def test_a_create_products(self):
        self.assertTrue(
            self.transformer_controller.create_new_product_on_blockchain(
                "Prodotto1 Test", [0, 2]
            )
        )
        self.assertIn(self.product_1, self.transformer_controller.get_all_products())
        self.assertEqual(self.product_1, self.transformer_controller.get_product(1))
        self.assertTrue(
            self.transformer_controller.create_new_product_on_blockchain(
                "Prodotto2 Test", [4, 6]
            )
        )
        self.assertIn(self.product_2, self.transformer_controller.get_all_products())
        self.assertEqual(self.product_2, self.transformer_controller.get_product(2))
        self.assertTrue(
            self.transformer_controller.create_new_product_on_blockchain(
                "Prodotto3 Test", [3, 5]
            )
        )
        self.assertIn(self.product_3, self.transformer_controller.get_all_products())
        self.assertEqual(self.product_3, self.transformer_controller.get_product(3))

    def test_b_add_transformation(self):
        self.product_1.cf += 50
        self.assertTrue(
            (self.transformer_controller.add_transformation_on_blockchain(50, 1, False))
        )
        self.assertEqual(
            self.product_1.cf, self.transformer_controller.get_product(1).cf
        )
        self.assertFalse(self.transformer_controller.get_product(1).is_ended)

    def test_c_transfer_product(self):
        self.product_2.address = self.transformer
        self.assertTrue(
            self.transformer_controller.transfer_product_on_blockchain(
                self.transformer, 2
            )
        )
        self.assertEqual(
            self.product_2.address, self.transformer_controller.get_product(2).address
        )

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_d_transfer_product_to_self_failed(self, mock_stdout):
        self.assertFalse(
            self.transformer_controller.transfer_product_on_blockchain(
                self.product_1.address, 1
            )
        )
        self.assertEqual(
            mock_stdout.getvalue(),
            "execution reverted: You cannot transfer the product to yourself. Transfer failed\n",
        )

    def test_e_final_transformation(self):
        self.product_1.cf += 100
        self.product_1.is_ended = True
        self.assertTrue(
            (self.transformer_controller.add_transformation_on_blockchain(100, 1, True))
        )
        self.assertEqual(
            self.product_1.cf, self.transformer_controller.get_product(1).cf
        )
        self.assertTrue(self.transformer_controller.get_product(1).is_ended)

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_f_create_product_failed_name_empty(self, mock_stdout):
        self.assertFalse(
            self.transformer_controller.create_new_product_on_blockchain("", [5, 9])
        )
        self.assertEqual(
            mock_stdout.getvalue(),
            "execution reverted: Product's name can't be empty\n",
        )
        self.assertNotIn(self.product_4, self.transformer_controller.get_all_products())

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_g_add_transformation_failed_is_ended(self, mock_stdout):
        self.product_1.cf += 50
        self.assertFalse(
            (self.transformer_controller.add_transformation_on_blockchain(50, 1, False))
        )
        self.assertEqual(
            mock_stdout.getvalue(),
            "execution reverted: The product is not modifiable anymore. Operation failed.\n",
        )
        self.assertNotEqual(
            self.product_1.cf, self.transformer_controller.get_product(1).cf
        )
        self.assertTrue(self.transformer_controller.get_product(1).is_ended)

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_h_transfer_product_failed(self, mock_stdout):
        self.product_1.address = self.transformer
        self.assertFalse(
            self.transformer_controller.transfer_product_on_blockchain(
                self.transformer, 1
            )
        )
        self.assertEqual(
            mock_stdout.getvalue(),
            "execution reverted: The product is not modifiable anymore. Transfer failed.\n",
        )
        self.assertNotEqual(
            self.product_1.address, self.transformer_controller.get_product(1).address
        )
        self.assertTrue(self.transformer_controller.get_product(1).is_ended)

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_i_add_transformation_failed_is_not_owner(self, mock_stdout):
        self.web3.eth.default_account = self.transformer
        self.product_3.cf += 50
        self.assertFalse(
            (self.transformer_controller.add_transformation_on_blockchain(50, 3, False))
        )
        self.assertEqual(
            mock_stdout.getvalue(),
            "execution reverted: To add a carbon footprint to a product you must be its owner. Operation failed.\n",
        )
        self.assertNotEqual(
            self.product_3.cf, self.transformer_controller.get_product(3).cf
        )

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_l_create_product_failed_not_rm_owner(self, mock_stdout):
        self.assertFalse(
            self.transformer_controller.create_new_product_on_blockchain(
                "Prodotto Misuse", [1, 7]
            )
        )
        self.assertEqual(
            mock_stdout.getvalue(),
            "execution reverted: A selected raw material is not property of the current user. Creation failed.\n",
        )
        self.assertNotIn(self.product_4, self.transformer_controller.get_all_products())


if __name__ == "__main__":
    unittest.main()
