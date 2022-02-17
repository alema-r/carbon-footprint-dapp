// SPDX-License-Identifier: GPL-3.0

//RIVEDERE

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract CarbonFootprint is ERC721{
    address public owner;
    uint256 productId = 0;

    // L'ordine qui è importante:
    // il mapping `allUsers` associa agli address un ruolo.
    // Di default il valore associato è 0, ciò significa che
    // un utente che non sia stato creato tramite `createUser`
    // avrà un ruolo pari a `NonRegistrato`.
    // Se ad esempio il primo della lista fosse `Fornitore`,
    // allora ogni utente di default avrebbe i privilegi di un fornitore.
    enum Role {NonRegistrato, Cliente, Fornitore, Trasformatore}

    struct Product {
        uint256 productId;
        string name;
        string rawMaterial;
        address currentOwner;
        //address[] owners;
        //uint[] cfs;
        uint CF;
        bool ended;
    }


    Product[] private allProducts;
    mapping(string => bool) productExists;
    mapping(address => Role) allUsers;

    event newCFAdded(address userAddress, uint cf, uint256 pId);

    ///
    //error userAlreadyExists(address senderAddress, Role currentRole);

    function createUser(uint role) public {
        require(allUsers[msg.sender] == Role.NonRegistrato, "L'utente ha gia' un ruolo");
        allUsers[msg.sender] = Role(role);
    }

    function getRole(address userAddress) public view returns(Role){
        require(userAddress!=address(0), "Indirizzo non valido.");
        require(allUsers[userAddress] != Role.NonRegistrato, "L'utente non e' registrato.");
        return allUsers[userAddress];
    }

    modifier onlyFornitore() {
        require(getRole(msg.sender) == Role.Fornitore);
        _;
    }

    modifier onlyTrasformatore() {
        require(getRole(msg.sender) == Role.Trasformatore);
        _;
    }

    constructor() ERC721("CarbonFootprintMonitor", "CFM"){
        owner = msg.sender;
    }

    function getAllProducts() public view returns (Product[] memory){
        return allProducts;
    }
 
    // Gestire via Python

    //function getMyProducts() public view returns (Product[] memory){
    //    Product[] memory ownedProducts;
    //    uint256 j = 0;
    //    for(uint256 i=0; i<allProducts.length; i++) {
    //        if(ownerOf(i) == msg.sender){
    //            ownedProducts.push(allProducts[i]);
    //            j++;
    //        }
    //    }
    //    return ownedProducts;
    //}

    // La variabile productId e' inizializzata a 0 e viene incrementata dopo aver inserito 
    // il prodotto nell'array. Quindi l'indice dell'array corrisponde al productId. 
    function getProductById(uint256 pId) public view returns (Product memory){
        return allProducts[pId];
    }

    // Gestire via Python

    // Restituisce la lista di tutti i prodotti finiti
    //function getFinishedProducts() public view returns (Product[] memory){
    //    Product[] memory finishedProducts;
    //    uint256 j = 0;
    //    for(uint256 i=0; i<allProducts.length; i++){
    //        if (allProducts[i].ended == true){
    //            finishedProducts[j] = allProducts[i];
    //            j++;
    //        }
    //    }
    //    return finishedProducts;
    //}

    function mintProduct(string calldata _productName, string calldata _rawMaterial, uint cf) public onlyFornitore {
        require(!productExists[_productName], "Il prodotto e' gia' presente.");

        _safeMint(msg.sender, productId);

        //address[] memory owners = new address[](1);
        //uint[] memory cfs = new uint[](1);
        //owners[0] = msg.sender;
        //cfs[0] = cf;
        //allProducts.push(Product(productId, _productName, _rawMaterial, msg.sender, owners, cfs, cf, false));

        allProducts.push(Product(productId, _productName, _rawMaterial, msg.sender, cf, false));
        productExists[_productName] = true;
        emit newCFAdded(msg.sender, cf, productId);

        productId++;
    }

    function addCF(uint partialCF, uint256 pId, bool isEnded) public onlyTrasformatore {
        Product storage productToUpdate = allProducts[pId];
        require(productToUpdate.ended == false, "Il prodotto non e' piu' modificabile.");
        require(productToUpdate.currentOwner == msg.sender, "Per aggiungere una carbon footprint al prodotto devi esserne il proprietario.");
        //productToUpdate.owners.push(msg.sender);
        //productToUpdate.cfs.push(partialCF);
        productToUpdate.CF += partialCF;
        emit newCFAdded(msg.sender, partialCF, pId);
        if(isEnded){
            productToUpdate.ended = true;
        }
    }

    // I clienti non posseggono Token, quindi non possono scambiarli
    function transferProduct(address toAddress, uint256 pId) public {
        Product storage productToUpdate = allProducts[pId];
        require(productToUpdate.ended == false, "Il prodotto non e' piu' modificabile.");
        require(getRole(toAddress) == Role.Trasformatore, "Il ruolo del destinatario deve essere: Trasformatore.");
        _safeTransfer(msg.sender, toAddress, pId, "");
        // la validità dell'indirizzo `toAddress` viene controllata dalla funzione `_safeTransfer` 
        productToUpdate.currentOwner = toAddress; 
    }
}
