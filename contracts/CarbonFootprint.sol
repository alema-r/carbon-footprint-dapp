// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.0 <0.9.0;
//pragma experimental SMTChecker;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./ProductLibrary.sol";
import "@openzeppelin/contracts/utils/Strings.sol";


/**
 * @title ERC721 contract to manage all products.
 * @notice Each product is actually an NFT.
 * @dev All functions should be called from the proxy contract `User`.
 */
contract CarbonFootprint is ERC721{
    // The address of the owner
    address public owner;

	// Variable that represent the id of a product
    uint256 private productId = 1;

    // Array that contains all products present in the contract.
    ProductLibrary.Product[] private allProducts;

    // Array that contains all rawmaterials present in the contract.
    ProductLibrary.RawMaterial[] private allRawMaterials;

    // Rivedere questo mapping nel caso in cui i prodotti possano avere lo stesso nome
    mapping(uint => uint) private RmToProduct;

    // Evento da emettere sulla blockchain quando viene aggiornata una carbon footprint
    /**
     * @notice Event used to track each carbon footprint addition.
     * @param userAddress The address of the user that adds the carbon footprint
     * @param cf The carbon footprint added.
     * @param pId The id of the updated product.
     */
	event newCFAdded(address userAddress, uint256 cf, uint256 pId);
    event newRawMaterialLotAdded(address userAddress, string name, uint256 lot, uint256 cf);
    event productIsFinished(address userAddress, uint256 pId, uint256 cf);
    event rawMaterialIsUsed(address transformer, address supplier, uint256 pId, string name, uint256 lot, uint256 cf);

    /**
     * @notice Initializes the contract and sets the `owner` to `msg.sender`.
     * @dev See {ERC721-constructor}
     */
	constructor() ERC721("CarbonFootprintMonitor", "CFM"){
        owner = msg.sender;
    }

    modifier onlyOwner{
        require(msg.sender == owner, "Errore! Invocazione anomala");
        _;
    }

    /**
     * @notice Returns all the products present in `allProducts`.
     * @return An array of `ProductLibrary.Product`.
     */
	function getAllProducts() public onlyOwner view returns (ProductLibrary.Product[] memory){
        return allProducts;
    }
    /**
     * @notice Returns all the rawmaterials present in `allRawMaterials`.
     * @return An array of `ProductLibrary.RawMaterial`.
     */
	function getAllRawMaterials() public onlyOwner view returns (ProductLibrary.RawMaterial[] memory){
        return allRawMaterials;
    }

    /**
     * @notice Returns the product with the specified `pId` id.
     * @dev Since `productId` is initialized to 0 and it is incremented by 1 
     * each time a new product is created, the id of a product matches 
     * the position in the `allProducts` array.
     * @param pId The id of the product.
     * @return A `ProductLibrary.Product` object.
     */
	function getProductById(uint256 pId) public onlyOwner view returns (ProductLibrary.Product memory){
        require(pId < productId, "Il prodotto non esiste");
        return allProducts[pId-1];
    }

    /**
     * @notice Creates a new rawmaterial with a specified name, lot and carboon footprint. It is called by the supplier who provides the rawm aterial
     * Then after checking the rawmaterial does not exist yet, it adds it to `allRawmaterial` and emits a `newRawMaterialLotAdded` event.
	 * @param _rawMaterialName Array with names of the rawmaterial provided.
	 * @param _lot Array with the rawmaterials' lot 
     * @param _cf Array with the rawmaterials' carboon footprint
     */
    function addRawMaterials(string[] calldata _rawMaterialName, uint256[] calldata _lot, uint256[] calldata _cf) public onlyOwner{
        require(_rawMaterialName.length == _lot.length, "Il numero delle materie prime non corrisponde al numero dei lotti");
        require(_rawMaterialName.length == _cf.length, "Il numero delle materie prime non corrisponde al numero delle carboon footprint");
        for(uint256 i = 0; i < _rawMaterialName.length; i++){
            bytes32 RmId = keccak256(bytes.concat(bytes(_rawMaterialName[i]), "-", bytes(Strings.toString(_lot[i])), "-", bytes20(tx.origin)));
            for(uint256 j = 0; j < allRawMaterials.length; j++){
                require(RmId != keccak256(bytes.concat(bytes(allRawMaterials[j].name), "-", bytes(Strings.toString(allRawMaterials[j].lot)), "-", bytes20(allRawMaterials[j].supplier))), "Hai gia' inserito questo lotto di questa materia prima");
            }
            allRawMaterials.push(ProductLibrary.RawMaterial(_rawMaterialName[i], _lot[i], tx.origin, _cf[i], false));
            emit newRawMaterialLotAdded(tx.origin, _rawMaterialName[i], _lot[i], _cf[i]);        
        }
    }

    /**
     * @notice Creates a product with specified product name, and specify rawmaterials transformer will use for the product.
     * Then it adds it to `allProducts` and emits a `newCFAddded` event.
     * @dev See {ERC721-_safeMint}
	 * @param _productName The name of the product.
	 * @param _index Array of indexes of the Rawmaterials in allRawMaterials
     */
	function mintProduct(
        string calldata _productName,
		uint256[] calldata _index
	) 
		public onlyOwner
	{       
        uint256 cf = 0;
        for(uint256 i = 0; i < _index.length; i++){
            require(allRawMaterials[_index[i]].isUsed == false, "Il lotto della materia prima inserita e' gia' stato utilizzato");
            assert(RmToProduct[_index[i]] == 0);
            RmToProduct[_index[i]] = productId;
            allRawMaterials[_index[i]].isUsed = true;
            cf += allRawMaterials[_index[i]].CF;
            emit rawMaterialIsUsed(tx.origin, allRawMaterials[_index[i]].supplier,productId, allRawMaterials[_index[i]].name, allRawMaterials[_index[i]].lot, allRawMaterials[_index[i]].CF);
        }
        //require(!productExists[_productName], "Il prodotto e' gia' presente.");
        //assert(!(_exists(productId)));
        _safeMint(tx.origin, productId);
        allProducts.push(ProductLibrary.Product(productId, _productName, tx.origin, cf, false));
        productId++;
    }

    /**
     * @notice Adds a carbon footprint to the specified product
     * @param partialCF The carbon footprint to be added.
     * @param pId The id of the product to be modified. 
     * @param isEnded Specify if this is the last transformation or not.
     */
	function addCF(uint256 partialCF, uint256 pId, bool isEnded) public onlyOwner{
        require(pId < productId, "Il prodotto non esiste");
        ProductLibrary.Product storage productToUpdate = allProducts[pId-1];
        require(productToUpdate.ended == false, "Il prodotto non e' piu' modificabile.");
        require(productToUpdate.currentOwner == tx.origin, "Per aggiungere una carbon footprint al prodotto devi esserne il proprietario.");
        assert(productToUpdate.productId < productId);
	productToUpdate.CF += partialCF;
        emit newCFAdded(tx.origin, partialCF, pId);
        if(isEnded){
            productToUpdate.ended = true;
            emit productIsFinished(tx.origin, pId, productToUpdate.CF);
        }
    }

    /**
     * @notice Transfer the property of a product with id `pId` to address `recipient`.
     * @dev Clients do not own any product so it's impossible for them to call this function.
     * The validity of the `recipient` address is checked by the `_safeTransfer` function. See
     * {ERC721-_safeTransfer}.
     * @param recipient The address to transfer the product property to
     * @param pId The id of the product to be transferred.
     */ 
	function transferProduct(address recipient, uint256 pId) public onlyOwner{
        require(pId < productId, "Il prodotto non esiste");
        require(pId > 0, "Il prodotto non esiste");
        ProductLibrary.Product storage productToUpdate = allProducts[pId-1];
        require(productToUpdate.ended == false, "Il prodotto non e' piu' modificabile.");
        _safeTransfer(tx.origin, recipient, pId, "");
        productToUpdate.currentOwner = recipient; 
    }
}
