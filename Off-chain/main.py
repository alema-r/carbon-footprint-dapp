import re
from connection import connect

ruolo = int(input("Specifica se sei un fornitore, un trasformatore o un cliente per richiedere delle operazioni: ").strip())
web3 = connect(ruolo)
print("Ecco le operazioni che puoi fare: ")
choice = ''
if ruolo == 0:
    # istanziazione oggetto che gestisce gli utenti di un ruolo
    while choice != 'E':
        print("Ricerca di uno o più prodotti(C)")
        print("Uscire(E)")
        choice = input("Digita una lettera per scegliere: ")
if ruolo == 1:
    # istanziazione oggetto che gestisce gli utenti di un ruolo
    while choice != 'E':
        print("Ricerca di uno o più prodotti(C)")
        print("Aggiunta di un nuovo prodotto(P)")
        print("Trasferimento del possesso di un prodotto(S)")
        print("Uscire(E)")
        choice = input("Digita una lettera per scegliere: ")
if ruolo == 2:
    # istanziazione oggetto che gestisce gli utenti di un ruolo
    while choice != 'E':
        print("Ricerca di uno o più prodotti(C)")
        print("Inserimento di una nuova trasformazione(T)")
        print("Trasferimento del possesso di un prodotto(S)")
        print("Uscire(E)")
        choice = input("Digita una lettera per scegliere: ")
print("Arrivederci")

