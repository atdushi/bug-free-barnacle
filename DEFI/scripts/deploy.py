import os
from brownie import accounts, USDC, AUSD, DefiBank, Contract
from dotenv import load_dotenv
load_dotenv()

def main():
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    
    # для ganache
    # account = accounts[0] 

    print(f"Account: {account}")
    
    usdc_addr = USDC.deploy({"from": account})
    ausd_addr = AUSD.deploy({"from": account})
    defi_addr = DefiBank.deploy(usdc_addr, ausd_addr, {"from": account})
    