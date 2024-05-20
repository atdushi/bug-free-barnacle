import os
from flask import Flask, jsonify, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField
from brownie import accounts, Contract, network
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# needed to keep the client-side sessions secure
app.config['SECRET_KEY'] = "C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb"

network.connect('sepolia')
usdcAddress = Contract(os.getenv("USDC_CONTRACT_ADDRESS"))
defi_contract = Contract(os.getenv("DEFI_CONTRACT_ADDRESS"))

account = accounts.add(os.getenv("PRIVATE_KEY"))
# to set up multiple accounts
# account1 = accounts.add(os.getenv("PRIVATE_KEY1"))
# account2 = accounts.add(os.getenv("PRIVATE_KEY2"))


class Form(FlaskForm):
    Faccounts = SelectField('Account', choices=[f'{account}'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/deposit')
def deposit():
    form = Form()
    AvailableBalance = sc_getAccountBalance() / 10 ** 18
    DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
    return render_template('deposit.html', form=form, AvailableBalance=AvailableBalance, DepositedAmount=DepositedAmount)


@app.route('/depositButton', methods=['GET', 'POST'])
def depositButton():
    form = Form()
    if request.method == 'POST':
        depositAmount = request.form.get("depositValue", type=int) * (10 ** 18)
        sc_depositBalance(depositAmount)
        DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
        AvailableBalance = usdcAddress.balanceOf(account) / (10 ** 18)
    return render_template('deposit.html', form=form,  AvailableBalance=AvailableBalance, DepositedAmount=DepositedAmount)


@app.route('/withdrawButton', methods=['GET', 'POST'])
def withdrawButton():
    form = Form()
    if request.method == 'POST':
        withdrawAmount = request.form.get(
            "withdrawValue", type=int) * (10 ** 18)
        sc_withdrawBalance(withdrawAmount)
        DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
        AvailableBalance = usdcAddress.balanceOf(account) / (10 ** 18)
    return render_template('deposit.html', form=form,  AvailableBalance=AvailableBalance, DepositedAmount=DepositedAmount)


def sc_withdrawBalance(withdrawAmount):
    defi_contract.withdraw(withdrawAmount, {"from": account})


def sc_getAccountBalance():
    balance = usdcAddress.balanceOf(account)
    return balance


def sc_depositBalance(depositAmount):
    usdcAddress.approve(defi_contract, depositAmount, {"from": account})
    defi_contract.depositToken(depositAmount, {"from": account})


@app.route('/refresh/<currentAccount>')
def refresh(currentAccount):
    global account
    account = accounts.at(currentAccount)
    currentBalance = usdcAddress.balanceOf(account) / (10 ** 18)
    stakedBalance = defi_contract.depositBalance(account) / (10 ** 18)
    return jsonify({'response': currentAccount, 'stakedBalance': stakedBalance, 'currentBalance': currentBalance})


@app.route('/FundMe', methods=["GET", "POST"])
def FundMe():
    if request.method == "POST":
        FromAddress = request.form.get("fromAddress")
        FromAddress = accounts.at(FromAddress, force=True)
        ToAddress = request.form.get("toAddress")
        Amount = request.form.get("Amount", type=int)
        usdcAddress.transfer(ToAddress, Amount * 10 **
                             18, {"from": FromAddress})
    return render_template('FundMe.html')


if __name__ == "__main__":
    app.run()
    network.disconnect()
