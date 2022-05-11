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
contract CarbonFootprint is ERC721 {
    // The address of the owner
    address public owner;

    // Variable that represents the id of a product
    uint256 private productId = 1;

    // Variable that represents the id of a raw material
    uint256 private materialId = 0;

    // Array that contains all products present in the contract.
    ProductLibrary.Product[] private allProducts;

    // Array that contains all rawmaterials present in the contract.
    ProductLibrary.RawMaterial[] private allRawMaterials;

    // Mapping used to track which raw materials has been used on which product.
    mapping(uint256 => uint256) private RmToProduct;

    /**
     * @notice Event used to track each carbon footprint addition.
     * @param userAddress The address of the user that adds the carbon footprint
     * @param cf The carbon footprint added.
     * @param pId The id of the updated product.
     */
    event newCFAdded(address userAddress, uint256 cf, uint256 pId);

    /**
     * @notice Event used to track each raw material addition.
     * @param supplierAddress The address of the supplier that adds the raw materials
     * @param transformerAddress The address of the trnasformer who receives the raw materials
     * @param mId The id of the raw material added
     * @param name The name of the raw material
     * @param lot The lot number
     * @param cf The carbon footprint of the raw material
     */
    event newRawMaterialLotAdded(
        address supplierAddress,
        address transformerAddress,
        uint256 mId,
        string name,
        uint256 lot,
        uint256 cf
    );

    /**
     * @notice Event used to track the completion of a product
     * @param userAddress The address of the transformer who completed the process
     * @param pId The id of the completed product
     * @param cf The total carbon footprint of the product
     */
    event productIsFinished(address userAddress, uint256 pId, uint256 cf);

    /**
     * @notice Event used to track when a raw material is used
     * @param transformer The address of the transformer that used the raw material
     * @param supplier The address of the supplier who supplied the raw material
     * @param pId The id of the product for which the raw material was used
     * @param mId The id of the used raw material
     * @param name The name of the used raw material
     * @param lot The lot number of the used raw material
     * @param cf The carbon footprint of the used raw material
     */
    event rawMaterialIsUsed(
        address transformer,
        address supplier,
        uint256 pId,
        uint256 mId,
        string name,
        uint256 lot,
        uint256 cf
    );

    /**
     * @notice Initializes the contract and sets the `owner` to `msg.sender`.
     * @dev See {ERC721-constructor}
     */
    constructor() ERC721("CarbonFootprintMonitor", "CFM") {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Error! Anomalous invocation");
        _;
    }

    /**
     * @notice Returns all the products present in `allProducts`.
     * @return An array of `ProductLibrary.Product`.
     */
    function getAllProducts()
        public
        view
        onlyOwner
        returns (ProductLibrary.Product[] memory)
    {
        return allProducts;
    }

    /**
     * @notice Returns all the rawmaterials present in `allRawMaterials`.
     * @return An array of `ProductLibrary.RawMaterial`.
     */
    function getAllRawMaterials()
        public
        view
        onlyOwner
        returns (ProductLibrary.RawMaterial[] memory)
    {
        return allRawMaterials;
    }

    /**
     * @notice Returns the product with the specified `pId` id.
     * @dev Since `productId` is initialized to 1 and it is incremented by 1
     * each time a new product is created, the id of a product matches
     * the position in the `allProducts` array shifted by 1.
     * @param pId The id of the product.
     * @return A `ProductLibrary.Product` object.
     */
    function getProductById(uint256 pId)
        public
        view
        onlyOwner
        returns (ProductLibrary.Product memory)
    {
        require(pId < productId && pId > 0, "Product doesn't exists");
        return allProducts[pId - 1];
    }

    /**
     * @notice Creates a new rawmaterial with a specified name, lot and carboon footprint. It is called by the supplier who provides the rawm aterial
     * Then after checking the rawmaterial does not exist yet, it adds it to `allRawmaterial` and emits a `newRawMaterialLotAdded` event.
     * @param _rawMaterialName Array with names of the rawmaterial provided.
     * @param _lot Array with the rawmaterials' lot
     * @param _cf Array with the rawmaterials' carboon footprint
     * @param _transformerAddress Address of the transformer who receives the raw material
     */
    function addRawMaterials(
        string[] calldata _rawMaterialName,
        uint256[] calldata _lot,
        uint256[] calldata _cf,
        address[] calldata _transformerAddress
    ) public onlyOwner {
        require(
            _rawMaterialName.length > 0,
            "No raw material names were provided. Insertion failed."
        );
        require(
            _lot.length > 0,
            "No raw material lots provided. Insertion failed."
        );
        require(
            _cf.length > 0,
            "No raw material carbon footprint provided. Insertion failed."
        );
        require(
            _transformerAddress.length > 0,
            "No transformer provided. Insertion failed."
        );
        require(
            _rawMaterialName.length == _lot.length,
            "The number of raw materials doesn't match the number of lots. Insertion failed."
        );
        require(
            _rawMaterialName.length == _cf.length,
            "The number of raw materials doesn't match the number of carbon footprints. Insertion failed."
        );
        require(
            _rawMaterialName.length == _transformerAddress.length,
            "The number of raw materials doesn't match the number of transformers. Insertion failed."
        );
        for (uint256 i = 0; i < _rawMaterialName.length; i++) {
            require(bytes(_rawMaterialName[i]).length > 0, "One or more raw material has an empty name");
            require(_cf[i] > 0, "One or more raw material has a carbon footprint value equal to 0");
            bytes32 RmHash = keccak256(
                bytes.concat(
                    bytes(_rawMaterialName[i]),
                    "-",
                    bytes(Strings.toString(_lot[i])),
                    "-",
                    bytes20(tx.origin)
                )
            );
            for (uint256 j = 0; j < allRawMaterials.length; j++) {
                require(
                    RmHash !=
                        keccak256(
                            bytes.concat(
                                bytes(allRawMaterials[j].name),
                                "-",
                                bytes(Strings.toString(allRawMaterials[j].lot)),
                                "-",
                                bytes20(allRawMaterials[j].supplier)
                            )
                        ),
                    "This lot of this raw material has been already inserted. Insertion failed."
                );
            }
            allRawMaterials.push(
                ProductLibrary.RawMaterial(
                    materialId,
                    _rawMaterialName[i],
                    _lot[i],
                    tx.origin,
                    _transformerAddress[i],
                    _cf[i],
                    false
                )
            );
            emit newRawMaterialLotAdded(
                tx.origin,
                _transformerAddress[i],
                materialId,
                _rawMaterialName[i],
                _lot[i],
                _cf[i]
            );
            materialId++;
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
    ) public onlyOwner {
        uint256 cf = 0;
        require(bytes(_productName).length > 0, "Product's name can't be empty");
        require(_index.length > 0, "No raw material selected. Creation failed");
        for (uint256 i = 0; i < _index.length; i++) {
            require(
                _index[i] < allRawMaterials.length,
                "Invalid raw material selected. Creation failed."
            );
            require(
                allRawMaterials[_index[i]].isUsed == false,
                "Inserted raw material's lot has already been used. Creation failed."
            );
            require(
                allRawMaterials[_index[i]].transformer == tx.origin,
                "A selected raw material is not property of the current user. Creation failed."
            );
            RmToProduct[_index[i]] = productId;
            allRawMaterials[_index[i]].isUsed = true;
            cf += allRawMaterials[_index[i]].CF;
            emit rawMaterialIsUsed(
                tx.origin,
                allRawMaterials[_index[i]].supplier,
                productId,
                allRawMaterials[_index[i]].materialId,
                allRawMaterials[_index[i]].name,
                allRawMaterials[_index[i]].lot,
                allRawMaterials[_index[i]].CF
            );
        }
        _safeMint(tx.origin, productId);
        allProducts.push(
            ProductLibrary.Product(
                productId,
                _productName,
                tx.origin,
                cf,
                false
            )
        );
        productId++;
    }

    /**
     * @notice Adds a carbon footprint to the specified product
     * @param partialCF The carbon footprint to be added.
     * @param pId The id of the product to be modified.
     * @param isEnded Specify if this is the last transformation or not.
     */
    function addCF(
        uint256 partialCF,
        uint256 pId,
        bool isEnded
    ) public onlyOwner {
        require(partialCF > 0, "You cannot add a carbon footprint lower than 1.");
        require(pId < productId && pId > 0, "The product doesn't exists. Operation failed.");
        ProductLibrary.Product storage productToUpdate = allProducts[pId - 1];
        require(productToUpdate.ended == false, "The product is not modifiable anymore. Operation failed.");
        require(
            productToUpdate.currentOwner == tx.origin,
            "To add a carbon footprint to a product you must be its owner. Operation failed."
        );
        productToUpdate.CF += partialCF;
        emit newCFAdded(tx.origin, partialCF, pId);
        if (isEnded) {
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
    function transferProduct(address recipient, uint256 pId) public onlyOwner {
        require(pId < productId, "The product doesn't exist. Transfer failed.");
        require(pId > 0, "The product doesn't exist. Transfer failed.");
        require(recipient != tx.origin, "You cannot transfer the product to yourself. Transfer failed");
        ProductLibrary.Product storage productToUpdate = allProducts[pId - 1];
        require(productToUpdate.ended == false, "The product is not modifiable anymore. Transfer failed.");
        _safeTransfer(tx.origin, recipient, pId, "");
        productToUpdate.currentOwner = recipient;
    }
}
