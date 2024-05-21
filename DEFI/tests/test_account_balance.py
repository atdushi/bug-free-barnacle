import os
from brownie import Contract, accounts
from dotenv import load_dotenv
load_dotenv()

def test_account_balance():
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    usdcAddress = Contract(os.getenv("USDC_CONTRACT_ADDRESS"))
    balance = usdcAddress.balanceOf(account)
    assert balance >= 0
    