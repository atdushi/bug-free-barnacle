// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../interfaces/IERC20.sol";

contract DefiBank {
    address public usdc;
    address public ausd;

    address[] public stakers;

    mapping(address => uint) public depositBalance;
    mapping(address => bool) public hasDeposited;

    constructor(address _usdc, address _ausd) {
        usdc = _usdc;
        ausd = _ausd;
    }

    function depositToken(uint _amount ) public {
        IERC20(usdc).transferFrom(msg.sender, address(this), _amount);
        depositBalance[msg.sender] +=  _amount;

        if(!hasDeposited[msg.sender]) {
            stakers.push(msg.sender);
        }

        hasDeposited[msg.sender] = true;
    }

    function withdraw(uint _amount) public {
        uint balance = depositBalance[msg.sender];
        require(balance > 0, "Balance cannot be 0");
        IERC20(usdc).transfer(msg.sender, _amount);

        depositBalance[msg.sender] -= _amount;

        if (balance - _amount == 0) {
            hasDeposited[msg.sender] = false;
        }
    }

    function issueInterest() public {
        for(uint i; i< stakers.length; i++) {
            address recipient = stakers[i];
            uint balance = depositBalance[recipient];

            if (balance > 0) {
                IERC20(ausd).transfer(recipient, balance);
            }
        } 
    }
}