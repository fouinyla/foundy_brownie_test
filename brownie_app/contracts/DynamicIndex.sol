// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DINDEX is ERC721URIStorage, Ownable {
    uint256 public tokenCounter;

    constructor () ERC721 ("Dynamic Index", "DINDEX"){
        tokenCounter = 0;
    }

    function createCollectible() public returns (uint256) {
        uint256 newItemId = tokenCounter;
        _safeMint(msg.sender, newItemId);
        tokenCounter = tokenCounter + 1;
        return newItemId;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public onlyOwner {
        _setTokenURI(tokenId, _tokenURI);
    }
}
