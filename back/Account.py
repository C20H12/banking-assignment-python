from SimpleDatabase import SimpleDb
from datetime import datetime
from json import dumps as JSON_stringify, loads as JSON_parse

# TODO: add false for isTesting
accountsDatabase = SimpleDb("data_files/accounts.txt")
balancesDatabase = SimpleDb("data_files/balances.txt")
transactionsDatabase = SimpleDb("data_files/transactions.txt")

class AccountError(Exception):
  pass

class Account:
  def __init__(self, username: str, password: str = '', asTransferTarget: bool = False):
    self.username = username
    self.password = password
    dataBaseEntry = accountsDatabase.getValue(self.username)
    self.exists = dataBaseEntry is not None
    self.authenticated = False
    self.balance = 0
    if not self.exists:
      return
    self.authenticated = dataBaseEntry == self.password
    if not self.authenticated:
      if asTransferTarget:
        self.authenticated = True
    self.balance = float(balancesDatabase.getValue(self.username) or 100)
  
  def _validateAccount(self):
    if self.exists is False:
      raise AccountError("Account does not exist")
    if self.authenticated is False:
      raise AccountError("Not authenticated")

  def saveAccount(self):
    self.exists = True
    self.authenticated = True
    accountsDatabase.insertValue(self.username, self.password)
    self.addTransaction(100, "initial balance, the benevolence")
  
  def _validateTransaction(self, amount):
    self._validateAccount()
    if self.balance < -amount:
      raise AccountError("Not enough funds")
    if amount == 0:
      raise AccountError("Zero amount")
  
  def getTransactions(self) -> list:
    transactions =  transactionsDatabase.getValue(self.username)
    if transactions == None:
      return []
    return JSON_parse(f"{transactions}")
    
  
  def addTransaction(self, amount: int, reason: str):
    self._validateTransaction(amount)
    self.balance += amount
    prevTransactions = self.getTransactions()

    formattedTime = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
    prevTransactions.append({
      "time": formattedTime,
      "amount": amount,
      "reason": reason,
      "balance": self.balance
    })
    transactionLogsStr = JSON_stringify(prevTransactions)
    transactionsDatabase.insertValue(self.username, transactionLogsStr)
    balancesDatabase.insertValue(self.username, self.balance)

  def transferTo(self, target: 'Account', amount: int):
    if target.exists is False:
      raise AccountError("Target does not exist")
    self.addTransaction(-amount, f"Transfer to {target.username}")
    target.addTransaction(amount, f"Transfer from {self.username}")

  def delete(self, password: str):
    self._validateAccount()
    if self.password != password:
      raise AccountError("Incorrect password")
    self.exists = False
    accountsDatabase.popEntry(self.username)
    transactionsDatabase.popEntry(self.username)
    balancesDatabase.popEntry(self.username)
  
  def changePassword(self, newPass: str):
    self._validateAccount()
    self.password = newPass
    accountsDatabase.insertValue(self.username, newPass)
  
