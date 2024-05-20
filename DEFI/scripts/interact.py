import os
from brownie import Contract, accounts
from dotenv import load_dotenv
load_dotenv()

def main():
    # Contract не работает в ganache
    
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    
    usdc_contract = Contract(os.getenv("USDC_CONTRACT_ADDRESS"))
    
    defi_contract = Contract(os.getenv("DEFI_CONTRACT_ADDRESS"))

    # print(f"totalSupply {usdc_contract.totalSupply() }")
    
    print(f"Before function call Current usdc token deposit balance is {defi_contract.depositBalance(account)}")
    
    usdc_contract.approve(defi_contract, 10000, {"from": account})
    
    defi_contract.depositToken(10000, {"from": account})

    print(f"After function call Current usdc token deposit balance is {defi_contract.depositBalance(account)}")
    
    defi_contract.withdraw(100, {"from": account})   

    print(f"Current balance after Withdraw usdc token deposit balance is {defi_contract.depositBalance(account)}")
