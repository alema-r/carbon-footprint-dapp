// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.0 <0.9.0;

/**
 * @title A library that contains a struct representing a product.
 */
library ProductLibrary{
    
	// Struct that represent a product
    struct Product {
        uint256 productId;
        string name;
        string rawMaterial;
        address currentOwner;
        uint256 CF;
        bool ended;
    }

}

