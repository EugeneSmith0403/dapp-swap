// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.0.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.0.0/contracts/token/ERC20/IERC20.sol";
import "./CreateToken.sol";


contract SwapVendor {
    mapping(address => bool) private tokens;
    address owner;

    constructor() {
        owner = msg.sender;
    }

    function addToken(address _address, uint256 liquidity) public {
        require(liquidity > 0, "Assign amount for liguidity!");
        require(msg.sender == owner, "Only owner can add token!");
        tokens[_address] = true;

        uint allowance = ERC20(_address).allowance(owner, address(this));
        require(allowance >= liquidity, "Check alowance!");

        ERC20(_address).transferFrom(owner, address(this), liquidity);
    }

    //   function getTokenList() public view returns(memory) {
    //       memory _tokens = tokens
    //       return _tokens;
    //   }


    function buyToken(address token) public payable {

        uint256 amountTobuy = msg.value;
        require(amountTobuy > 0, "You haven't got ETH!");

        uint256 curBalance = ERC20(token).balanceOf(address(this));
        require(curBalance > 0, "Current token balance 0!");

        ERC20(token).transfer(msg.sender, amountTobuy);
    }

    function sellToken(address token, uint amount) public payable {
        uint256 userBalance = ERC20(token).balanceOf(msg.sender);
        require(userBalance > 0, "Balance of current token equals 0!");

        uint256 contractBalance = ERC20(token).balanceOf(address(this));
        require(contractBalance > 0, "Ligudity equals 0!");

        uint allowance = ERC20(token).allowance(msg.sender, address(this));
        require(allowance >= amount, "Check alowance!");

        ERC20(token).transferFrom(msg.sender, address(this), amount);
        payable(msg.sender).transfer(amount);

    }


    function swap(address sailedToken, uint256 sailedAmount,
        address boughtToken) public payable {

        bool checkSailToken = tokens[sailedToken];
        bool checkBuyToken = tokens[boughtToken];

        uint currentPaymentWei = MyToken(sailedToken).calculateTotalSum(sailedAmount);

        uint buyAmount = MyToken(boughtToken).calculateTotalAmountsOfCoin(currentPaymentWei);

        MyToken sToken = MyToken(sailedToken);
        MyToken bToken = MyToken(boughtToken);

        require(checkSailToken, "Token, which you want sail, doesn't exist!");
        require(checkBuyToken, "Token, which you want buy, doesn't exist!");

        uint256 getBalanceOfContractForSailedToken = sToken.balanceOf(address(this));
        uint256 getBalanceOfContractForBuyToken = bToken.balanceOf(address(this));

        require(getBalanceOfContractForSailedToken > 0, "Contract hasn't got coins of sailed token!");
        require(getBalanceOfContractForBuyToken > 0, "Contract hasn't got coins of buy token!");

        uint allowanceSailedToken = ERC20(sToken).allowance(msg.sender, msg.sender);
        require(allowanceSailedToken >= currentPaymentWei, "Check alowance sailed token!");

        (bool sentSailedToken) = sToken.transferFrom(msg.sender, address(this), sailedAmount);
        require(sentSailedToken, "Failed to transfer sailed tokens from user to contract!");

        uint allowanceBuyToken = ERC20(bToken).allowance(msg.sender, address(this));
        require(allowanceBuyToken >= buyAmount, "Check alowance buy token!");

        (bool sentBuyToken) = bToken.transferFrom(address(this), msg.sender, buyAmount);
        require(sentBuyToken, "Failed to transfer buy tokens from contract to user!");
    }

}
