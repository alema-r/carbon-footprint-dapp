from attr import validate
from Utils import lot_input_validation
from Utils import input_validation
from Utils import carbon_fp_input_validation
from Utils import address_validation
from Utils import raw_material_name_input_validation
from Utils import Raw_material
import inquirer
from BlockChain import create_product_on_blockchain
from BlockChain import transfer_cp
from BlockChain import create_raw_materials_on_blockchain



def insert_raw_material(contract, user_address):
    raw_materials = []
    actions = ""
    '''
    product_name = inquirer.text(
       message = "Insert new product's name",
       # lambda function che controlla che nel nome ci siano solo caratteri alfanumerici 
       validate = product_name_input_validation
    )
    carbon_fp = inquirer.text(
        message= "Insert carbon footprint",
        # controlla se il numero inserito è un intero
        validate = carbon_fp_input_validation
    )
    '''
    while (actions != "Done") & (actions != "Cancel"):
        actions = inquirer.list_input(
            message= "Select \"Add new raw material\" to add new material or select \"Done\" to complete operation or select \"Cancel\" to cancel the operation",
            choices=["Add new raw material", "Done", "Cancel"]
        )
        if actions == "Add new raw material":
            questions = [
            inquirer.Text('raw material',
            message="Insert new raw material name",
            validate=raw_material_name_input_validation
            ),
            inquirer.Text('lot',
            message="Insert raw material's lot",
            validate=lot_input_validation
            ),
            inquirer.Text('carbon footprint',
            message = "Insert raw material carbon footprint",
            validate=carbon_fp_input_validation
            )
            ]
            # Il propt salva le risposte in un dizionario dove la chiave è la domanda e il valore è la risposta dell'utente
            answers = inquirer.prompt(questions)
            raw_material_to_check = Raw_material(answers["raw material"], int(answers['lot']), user_address, int(answers['carbon footprint']))
            # Una volta ricevute le risposte esse vanno validate e sanificate.
            valid, error_message = input_validation(raw_material_to_check, raw_materials, answers) 
            if valid:
                raw_materials.append(raw_material_to_check)
                print("New raw material correctly inserted")
                print("To add another raw material select \"Add new raw material\" or select \"Done\" to complete the operation")
            else:
                print(f"Invalid input: {error_message}")
                print('Select \"Add new raw material\" and try again or selcet \"Cancel\" to cancel the operation') 
    
    # Se l'operazione viene annullata la funzione termina
    if actions == "Cancel":
        raw_materials = []
        return
    
    # Una volta finito l'inserimento delle materie prime per il prodotto e per il lotto si può chiamare la funzione per inserire
    # il nuovo prodotto sulla blockchain
    if (len(raw_materials) > 0):
        try:
            #create_product_on_blockchain(contract, product_name, raw_materials, int(carbon_fp))
            create_raw_materials_on_blockchain(contract, raw_materials)
        except Exception as e:
            # TODO: migliorare il meccanimo di interazione con l'utente e di risposta agli errori.
            print(e)