import Supplier
import Transformer

role_dict = {
    "Client": {
        "num": "0",
        "actions": {"Search one or more products": lambda a: a,  # get_filtered_products,
                    "Exit": exit
                    },
    },
    "Supplier": {
        "num": "1",
        "actions": {
            "Search one or more products": lambda a: a,
            "Add new raw materials": Supplier.insert_raw_material,
            "Exit": exit,
            },
    },
    "Transformer": {
        "num": "2",
        "actions": {
            "Search one or more products": lambda a: a,
            "Create a new product": Transformer.create_new_product,
            "Add a new operation": Transformer.add_transformation,
            "Transfer the property of a product": Transformer.transfer_product,
            "Exit": exit,
        },
    },
}