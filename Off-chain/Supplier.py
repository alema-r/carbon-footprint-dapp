from Utils import raw_material_input_validation
from Utils import lot_input_validation
from Utils import input_validation
from Utils import carbon_fp_input_validation
from Utils import address_validation
import inquirer
from BlockChain import create_product_on_blockchain
from BlockChain import transfer_cp

def create_product(contract):
    raw_materials = []
    lots = []
    product_name = inquirer.text(
       message = "Insert new product's name",
       # lambda function che controlla che nel nome ci siano solo caratteri alfanumerici 
       validate = lambda _, name: any(not c.isalnum() for c in name)
    )
    carbon_fp = inquirer.text('carbon footprint',
        message= "Insert carbon footprint",
        # controlla se il numero inserito è un intero
        validate = carbon_fp_input_validation
    )

    while actions != "Done":
        actions = inquirer.input_list(
            message= "Select \"Add new raw material\" to add new material or select \"Done\" to complete operation",
            choices=["Add new raw material", "Done"]
        )
        if actions == "Add new raw material":
            questions = [
            inquirer.Text('raw material',
            message="Insert new raw material",
            validate=raw_material_input_validation
            ),
            inquirer.Text('lot',
            message="Insert raw material's lot",
            validate=lot_input_validation
            )
            ]
            # Il propt salva le risposte in un dizionario dove la chiave è la domanda e il valore è la risposta dell'utente
            answers = inquirer.prompt(questions)
            # Una volta ricevute le risposte esse vanno validate e sanificate.
            valid, error_message = input_validation(raw_materials, lots, answers) 
            if valid:
                raw_materials.append(answers["raw material"])
                lots.append(int(answers['lot']))
                print("New raw material correctly inserted")
                print("To add another raw material select \"Add new raw material\" or select \"Done\" to complete the operation")
            else:
                print(f"Invalid input: ${error_message}")
                print('Select \"Add new raw material\" and try again') 
            
    
    # Una volta finito l'inserimento delle materie prime per il prodotto e per il lotto si può chiamare la funzione per inserire
    # il nuovo prodotto sulla blockchain
    if (len(raw_materials) > 0 & len(lots) > 0):
        try:
            create_product_on_blockchain(contract, product_name, raw_materials, lots, carbon_fp)
        except Exception as e:
            # TODO: migliorare il meccanimo di interazione con l'utente e di risposta agli errori.
            print("Product not created, error occured")
    # Vedere come viene trattate l'eccezione durante la validazione
        
        
            
def transfer_product(contract):
    recipient = inquirer.text(
        message = "Insert recipient address",
        # Controlla che il recipient inserito sia nel formato corretto
        validate = address_validation
    )
    # TODO: capire come trattare il token_id, se farlo inserire dal produttore o ritrovarlo sulla blockchain
    # probabilmente l'opzione migliore è permettere al supplier di ritrovare tutti i prodotti che sono a lui associati.

    # transfer_cp()


    pass