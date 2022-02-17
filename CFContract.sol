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
        address[] owners;
        uint[] cfs;
        uint finalCF;
        bool ended;
    }


    Product[] public allProducts;
    mapping(string => bool) productExists;
    mapping(address => Role) allUsers;

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
 
    function getMyProducts() public view returns (Product[] memory){
        Product[] memory ownedProducts;
        uint256 j = 0;
        for(uint256 i=0; i<allProducts.length; i++) {
            if(ownerOf(i) == msg.sender){
                ownedProducts[j] = allProducts[i];
                j++;
            }
        }
        return ownedProducts;
    }

    // La variabile productId e' inizializzata a 0 e viene incrementata dopo aver inserito 
    // il prodotto nell'array. Quindi l'indice dell'array corrisponde al productId. 
    function getProductById(uint256 pId) public view returns (Product memory){
        return allProducts[pId];
    }

    // Restituisce la lista di tutti i prodotti finiti
    function getFinishedProducts() public view returns (Product[] memory){
        Product[] memory finishedProducts;
        uint256 j = 0;
        for(uint256 i=0; i<allProducts.length; i++){
            if (allProducts[i].ended == true){
                finishedProducts[j] = allProducts[i];
                j++;
            }
        }
        return finishedProducts;
    }

    function mintProduct(string calldata _productName, string calldata _rawMaterial, uint cf) public onlyFornitore {
        require(!productExists[_productName], "Il prodotto e' gia' presente.");

        _safeMint(msg.sender, productId);

        address[] memory owners = new address[](1);
        uint[] memory cfs = new uint[](1);
        owners[0] = msg.sender;
        cfs[0] = cf;

        allProducts.push(Product(productId, _productName, _rawMaterial, msg.sender, owners, cfs, cf, false));

        productExists[_productName] = true;

        productId++;        
    }

    function addCF(uint partialCF, uint256 pId, bool isEnded) public onlyTrasformatore {
        Product storage productToUpdate = allProducts[pId];
        require(productToUpdate.ended == false, "Il prodotto non e' piu' modificabile.");
        require(productToUpdate.currentOwner == msg.sender, "Per aggiungere una carbon footprint al prodotto devi esserne il proprietario.");
        productToUpdate.owners.push(msg.sender);
        productToUpdate.cfs.push(partialCF);
        productToUpdate.finalCF += partialCF;
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
        productToUpdate.currentOwner = toAddress; 
    }
}
