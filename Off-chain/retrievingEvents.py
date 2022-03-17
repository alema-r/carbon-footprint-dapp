import json
import asyncio
import inquirer
from pandas import DataFrame
from _datetime import datetime

from web3 import Web3
from web3.middleware import geth_poa_middleware

baseURL = "http://127.0.0.1:22000"

# Funzione con istruzioni replicate per andare a connetersi alla blockchain
def connnectionUtils(URL):
    web3 = Web3(Web3.HTTPProvider(URL))
    abiUser = json.loads(
        '[{"inputs":[{"internalType":"address","name":"defaultSupplier","type":"address"},{"internalType":"address","name":"defaultTransformer","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"enum User.Role","name":"role","type":"uint8"}],"name":"newUser","type":"event"},{"inputs":[],"name":"CFaddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"carbon_fp","type":"uint16"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bool","name":"isEnded","type":"bool"}],"name":"addTransformation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"product_name","type":"string"},{"internalType":"string[]","name":"raw_material","type":"string[]"},{"internalType":"uint256[]","name":"lots","type":"uint256[]"},{"internalType":"uint256","name":"carbon_fp","type":"uint256"}],"name":"createProduct","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint8","name":"role","type":"uint8"}],"name":"createUser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getProducts","outputs":[{"components":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"address","name":"currentOwner","type":"address"},{"internalType":"uint256","name":"CF","type":"uint256"},{"internalType":"bool","name":"ended","type":"bool"}],"internalType":"struct ProductLibrary.Product[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getRole","outputs":[{"internalType":"enum User.Role","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRole","outputs":[{"internalType":"enum User.Role","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferCP","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
    abiCF = json.loads(
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"cf","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"pId","type":"uint256"}],"name":"newCFAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"string","name":"RmId","type":"string"},{"indexed":false,"internalType":"uint256","name":"pId","type":"uint256"}],"name":"newRawMaterialLotAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"pId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"cf","type":"uint256"}],"name":"productIsFinished","type":"event"},{"inputs":[{"internalType":"uint256","name":"partialCF","type":"uint256"},{"internalType":"uint256","name":"pId","type":"uint256"},{"internalType":"bool","name":"isEnded","type":"bool"}],"name":"addCF","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAllProducts","outputs":[{"components":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"address","name":"currentOwner","type":"address"},{"internalType":"uint256","name":"CF","type":"uint256"},{"internalType":"bool","name":"ended","type":"bool"}],"internalType":"struct ProductLibrary.Product[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAllRawMaterials","outputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"lot","type":"uint256"}],"internalType":"struct ProductLibrary.RawMaterial[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"pId","type":"uint256"}],"name":"getProductById","outputs":[{"components":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"address","name":"currentOwner","type":"address"},{"internalType":"uint256","name":"CF","type":"uint256"},{"internalType":"bool","name":"ended","type":"bool"}],"internalType":"struct ProductLibrary.Product","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_productName","type":"string"},{"internalType":"string[]","name":"_rawMaterial","type":"string[]"},{"internalType":"uint256[]","name":"_lots","type":"uint256[]"},{"internalType":"uint256","name":"cf","type":"uint256"}],"name":"mintProduct","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"pId","type":"uint256"}],"name":"transferProduct","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
    address = web3.toChecksumAddress("0x1932c48b2bF8102Ba33B4A6B545C32236e342f34")
    userContract = web3.eth.contract(address=address, abi=abiUser)
    addressCF = userContract.functions.CFaddress().call()
    CFContract = web3.eth.contract(address=addressCF, abi=abiCF)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3, CFContract


def retrievingProductData(productID):
    web3, CFContract = connnectionUtils(baseURL)
    # Recupero dall'abi del contratto CFContract i metadati che descrivono gli eventi
    events_metadata = [abi for abi in CFContract.abi if abi["type"] == "event"]
    # Preparo un dizionario che dovrà contenere gli hash delle firme degli eventi
    event_signatures_hex = dict()
    # inizializzo delle strutture dati per le informazioni estratte dai log
    materiePrime = []
    trasformazioni = []
    isFinished = [False, 0, 0]
    supplier = None
    RawMaterialCf = None
    # colleziono solo i metadati degli eventi che mi interessano
    for event_metadata in events_metadata:
        # Registro il nome dell'evento
        name = event_metadata["name"]
        # Registro i parametri di input dell'evento in una lista
        inputs = [param["type"] for param in event_metadata["inputs"]]
        # Poi creo una stringa con tutti questi separati da virgole
        inputs = ",".join(inputs)
        # Ri-Creo la firma dell'evento così come è scritta nel codice solidity
        event_signature_text = f"{name}({inputs})"
        # Ricavo l'hash di questa firma che mi permetterà di identificare univocamente gli eventi nei
        # log delle transazioni
        event_signatures_hex.update({name: web3.toHex(web3.keccak(text=event_signature_text))})
    # prendo il numero dell'ultimo blocco
    latest = web3.eth.blockNumber
    # itero su tutti i blocchi forgiati nella blockchain
    for i in range(1, latest+1):
        # registro la data e l'ora in cui è stata fatta la transazione ed emessi gli eventi
        time = datetime.fromtimestamp(web3.eth.getBlock(i)['timestamp'] // 10**9)
        # recupero la transazione contenuta nel blocco i-esimo
        tx = web3.eth.get_transaction_by_block(i, 0)
        # usando l'hash della transazione recupero la ricevuta associata
        tx_receipt = web3.eth.get_transaction_receipt(tx['hash'])
        # se ci sono dei log all'interno della ricevuto itero su questi
        if len(tx_receipt['logs']) > 0:
            for log in tx_receipt['logs']:
                # recupero l'hash della firma dell'evento contenuto nel log corrente della ricevuta
                receipt_event_signature_hex = web3.toHex(log["topics"][0])
                # Controllo se l'hash della firma dell'evento recuperato coincide con uno degli hash
                # degli eventi mi interessano e che ho ricreato prima. In caso processo il log per
                # ottenere i dati sull'evento e lo inserisco in una delle strutture date apposite
                if receipt_event_signature_hex == event_signatures_hex["newCFAdded"]:
                    processed_log = CFContract.events.newCFAdded().processLog(log)
                    event = processed_log['args']
                    if event['pId'] == productID:
                        # inserisco un ulteriore controllo per non includere tra le trasformazioni
                        # stampate, l'evento corrispondente all'aggiunta della carboon footprint delle
                        # materie prime
                        if event['userAddress'] == supplier:
                            RawMaterialCf = event['cf']
                        else:
                            trasformazioni.append([event["userAddress"], event['pId'], event['cf'], time])
                elif receipt_event_signature_hex == event_signatures_hex["newRawMaterialLotAdded"]:
                    processed_log = CFContract.events.newRawMaterialLotAdded().processLog(log)
                    event = processed_log['args']
                    if event['pId'] == productID:
                        # valorizzo l'indirizzo del fornitore considerando il campo userAddress del
                        # primo evento newCFAdded relativo al productID del prodotto
                        # DARIVEDERE PERCHE' NON SONO SICURO
                        if supplier is None:
                            supplier = event['userAddress']
                        RawMaterial = str(event["RmId"]).rsplit('-')[0]
                        Lot = str(event["RmId"]).rsplit('-')[1]
                        materiePrime.append([RawMaterial, Lot, time])
                elif receipt_event_signature_hex == event_signatures_hex["productIsFinished"]:
                    processed_log = CFContract.events.productIsFinished().processLog(log)
                    event = processed_log['args']
                    if event['pId'] == productID:
                        # valorizzo una lista che mi serve per la stampa delle informazioni sulla
                        # conclusione del prodotto
                        isFinished = [True, event['cf'], time]
    # utilizzo di pandas per la stampa delle tabelle con le informazioni su un determinato prodotto
    # Preparo le intestazioni per le due tabelle una relativa alle materie prime e una relativa alle
    # trasformazioni
    headersRm = ["Raw Material", "Lot", "Date"]
    headersTr = ["Transformer", "ProductID", "Carboon Footprint", "Date"]
    print(f"Raw materials used for this product are provided by supplier {supplier} and their carboon footprint is {RawMaterialCf}")
    print()
    print(DataFrame(materiePrime, columns=headersRm))
    print()
    print("-----------------------------------------------------------------")
    print()
    if len(trasformazioni) > 0:
        print("These are transformations done on the product until now:")
        print()
        print(DataFrame(trasformazioni, columns=headersTr))
        print()
    else:
        print("There aren't yet transformations done on this product:")
        print()
    print('-----------------------------------------')
    print()
    if isFinished[0]:
        print(f"No more transformation are needed. The product was completed on {isFinished[2]} and its carboon footprint is {isFinished[1]}")

# parte per l'ascolto degli eventi quando vengono emessi


'''loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(block_filter, 2, web3)))
                #log_loop(tx_filter, 2)))
    finally:
        loop.close()'''

'''def handle_event(event):
    print(Web3.toJSON(event))

async def log_loop(event_filter, poll_interval, web3):
    while True:
        for newCFAdded in event_filter.get_new_entries():
            handle_event(newCFAdded, web3)
        await asyncio.sleep(poll_interval)'''


if __name__ == "__main__":
    pid = int(inquirer.text(
        message="Please Insert Product ID",
    ))
    retrievingProductData(pid)
