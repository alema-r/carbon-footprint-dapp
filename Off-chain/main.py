import re

userAddress = input("Benvenuto, per iniziare inserisci il tuo portafoglio elettronico: ").strip()
while not re.match("^0x[A-Za-z0-9]{40}$", userAddress):
    print("Il formato dell'indirizzo inserito non è corretto. Inserire un nuovo indirizzo")
    userAddress = input("Inserisci il tuo portafoglio elettronico: ").strip()
"""Ruolo = input("Specifica se sei un fornitore, un trasformatore o un cliente per richiedere delle operazioni: ").strip()"""

