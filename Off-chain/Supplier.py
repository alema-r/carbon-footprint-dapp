from email import message
from attr import validate
import inquirer

def create_product():
    raw_material = []
    lots = []
    j
    product_name = inquirer.Text(
       message = "Insert new product's name" 
    )

    while actions != "Done":
        actions = inquirer.input_list(
            message= "Select new raw material to add new material or select done to complete operation",
            choices=["Add new raw material", "Done"]
        )
        if actions == "Add new raw material":
            raw_material = inquirer.text('raw material',
            message="Insert new raw material",
            validate=raw_material_input_validation()
            )

            lot = inquirer.text('lot',
            message="Insert raw material's lot",
            validate=lot_input_validation()
            )
        # Vedere come viene trattate l'eccezione durante la validazione
        
        
            
def transfer_product():
    pass