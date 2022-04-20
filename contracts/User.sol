// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.0 <0.9.0;
//pragma experimental SMTChecker;

import "./ProductLibrary.sol";
import "./CarbonFootprint.sol";

/**
 * @title A proxy for `CarbonFootprint` contract that also manages users.
 * @notice A user can use this contract to manage carbon footprints of all products.
 * @dev The owner of the `CarbonFootprint` contract is this contract.
 */
contract User {
    // enum variable to manage users' role
    enum Role {
        NotRegistered,
        Supplier,
        Transformer
    }
    Role constant supplier = Role.Supplier;
    Role constant transformer = Role.Transformer;
    Role constant defaultChoice = Role.NotRegistered;

    /**
     * @dev Initializes the `CarbonFootprint` contract.
     */
    CarbonFootprint CFContract = new CarbonFootprint();
    address public CFaddress = address(CFContract);

    // Mapping each user address to a role
    mapping(address => Role) private _users;

    // Address of the contract owner
    address private owner;

    /**
     * @notice Event used to track when a new user is registered
     * @param userAddress The address of the new user
     * @param role The role of the new user
     */
    event newUser(address userAddress, Role role);

    /**
     * @dev Initializes the contract by setting a default supplier and a default
     * transformer.	Also it sets the `owner` of the contract to `msg.sender`.
     */
    constructor(address defaultSupplier, address defaultTransformer) {
        owner = msg.sender;
        require(defaultSupplier != defaultTransformer);
        _users[defaultSupplier] = supplier;
        _users[defaultTransformer] = transformer;
        emit newUser(defaultSupplier, supplier);
        emit newUser(defaultTransformer, transformer);
    }

    /**
     * @notice Retrieves the role of `msg.sender`.
     * @return The role of the address specified.
     */
    function getRole() public view returns (Role) {
        return _users[msg.sender];
    }

    /**
     * @notice Retrieves the role of the address specified.
     * @param wallet The address of the user that you want to retrieve the role.
     * @return The role of the address specified.
     */
    function getRole(address wallet) public view returns (Role) {
        require(wallet != address(0), "Invalid address");
        return _users[wallet];
    }

    /**
     * @notice Function that associate the Role `role` to `msg.sender`.
     * @param role The role to set. (1=Supplier, 2=Transformer).
     */
    function createUser(uint8 role) external {
        require(
            _users[msg.sender] == defaultChoice,
            "The user already has a role"
        );
        _users[msg.sender] = Role(role);
        emit newUser(msg.sender, _users[msg.sender]);
    }

    // Modificatori necessari per il controllo sulle funzioni
    modifier onlySupplier() {
        require(getRole() == supplier);
        _;
    }

    modifier onlyTransformer() {
        require(getRole() == transformer);
        _;
    }

    /**
     * @notice Creates a product with specified name, raw material and initial carbon footprint.
     * @dev Calls the function `mintProduct` from `CarbonFootprint` contract.
     * @param product_name The name to assign to the product.
     * @param materialIds The ids of the raw materials used to create the product
     */
    function createProduct(
        string calldata product_name,
        uint256[] calldata materialIds
    ) external onlyTransformer {
        CFContract.mintProduct(product_name, materialIds);
    }

    /**
     * @notice Creates a product with specified name, raw material and initial carbon footprint.
     * @dev Calls the function `addRawMaterials` from `CarbonFootprint` contract.
     * @param name The array of the raw materials' name.
     * @param lot The array of the raw materials' lot.
     * @param cf The array of the raw materials' carbon footprint.
     * @param transformerAddress The array of the transformer that will receive the respective lots of raw materials.
     */
    function createRawMaterials(
        string[] calldata name,
        uint256[] calldata lot,
        uint256[] calldata cf,
        address[] calldata transformerAddress
    ) external onlySupplier {
        CFContract.addRawMaterials(name, lot, cf, transformerAddress);
    }

    /**
     * @notice Add a carbon footprint relating to transformer actions.
     * @dev Calls the function `addCF` from `CarbonFootprint` contract.
     * @param carbon_fp The carbon footprint relating to transformer actions.
     * @param tokenId The id of the product to add the carbon footprint to.
     * @param isEnded Specifies if this is the last transformation.
     */
    function addTransformation(
        uint16 carbon_fp,
        uint256 tokenId,
        bool isEnded
    ) external onlyTransformer {
        CFContract.addCF(carbon_fp, tokenId, isEnded);
    }

    /**
     * @notice Transfer the ownership of the product with product id `tokenId` to the address `recipient`
     * @param recipient The address of the recipient to transfer the product to.
     * @param tokenId The id of the product to be transferred.
     */
    function transferCP(address recipient, uint256 tokenId) external {
        require(
            getRole(recipient) == transformer,
            "Recipient's role must be: Transformer"
        );
        CFContract.transferProduct(recipient, tokenId);
    }

    /**
     * @notice Returns all the products currently present in `CarbonFootprint` contract
     * @return An array of `ProductLibrary.Product`.
     */
    function getProducts()
        external
        view
        returns (ProductLibrary.Product[] memory)
    {
        return CFContract.getAllProducts();
    }

    /**
     * @notice Returns the product with the specified `pId` id.
     * @param productId The id of the product.
     * @return A `ProductLibrary.Product` object.
     */
    function getProductById(uint256 productId)
        external
        view
        returns (ProductLibrary.Product memory)
    {
        return CFContract.getProductById(productId);
    }

    /**
     * @notice Returns all the products currently present in `CarbonFootprint` contract
     * @return An array of `ProductLibrary.Product`.
     */
    function getRawMaterials()
        external
        view
        returns (ProductLibrary.RawMaterial[] memory)
    {
        return CFContract.getAllRawMaterials();
    }
}
