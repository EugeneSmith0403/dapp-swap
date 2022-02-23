// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "@baseOpenzeppelin/@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is Context, ERC20 {

    address public creator;
    uint price = 1 * 10 ** 18;
    uint constant ETH_PRICE = 1 * 10 ** 18;

    constructor(
        string memory name,
        string memory symbol,
        uint256 _amount,
        uint256 partialPrice
    ) ERC20(name, symbol) {
        creator = msg.sender;
        price = price * partialPrice * _amount;
        _mint(creator, price);
    }

    function setPrice(uint _price) public {
        price = _price;
    }

    function getPrice() public view returns(uint) {
        return price;
    }

    function calculateTotalSum(uint _amountCoins) public view returns(uint) {
        return _amountCoins * price;
    }

    function calculateTotalAmountsOfCoin(uint weiCount) public view returns(uint) {
        return weiCount / price * ETH_PRICE;
    }
}
