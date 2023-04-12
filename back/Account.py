from SimpleDatabase import SimpleDb
from datetime import datetime

# TODO: add false for isTesting
accountsDatabase = SimpleDb("data_files/accounts.txt")
balancesDatabase = SimpleDb("data_files/balances.txt")
transactionsDatabase = SimpleDb("data_files/transactions.txt")

class Account:
  def __init__(self, username: str, password: str = '', asTransferTarget: bool = False):
    self.username = username
    self.password = password
    self.balance = 100
    self.exists = accountsDatabase.getValue(self.username) is not None
    if not self.exists:
      return
    self.authenticated = accountsDatabase.getValue(self.username) == self.password
    if not self.authenticated:
      if asTransferTarget:
        self.authenticated = True
      return
    self.balance = int(balancesDatabase.getValue(self.username))
  
  def validateAccount(self):
    if self.exists is False:
      raise Exception("account_does_not_exist")
    if self.authenticated is False:
      raise Exception("not_authenticated")

  def saveAccount(self):
    self.exists = True
    self.authenticated = True
    return accountsDatabase.insertValue(self.username, self.password)
  
  def validateTransaction(self, amount):
    self.validateAccount()
    if self.balance < -amount:
      raise Exception("not_enough_money")
    if amount == 0:
      raise Exception("zero_amount")
  
  def getTransactions(self):
    return transactionsDatabase.getValue(self.username)
  
  def addTransaction(self, amount: int, reason: str):
    self.validateTransaction(amount)
    self.balance += amount
    formattedTime = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
    transactionLogStr = \
      f'''{{"time": "{formattedTime}", "amount": {amount}, "reason": {reason}, "balance": {self.balance}}}'''
    prevTransactions = self.getTransactions()
    prevTransactions = prevTransactions + ',' if prevTransactions is not None else ""
    transactionsDatabase.insertValue(self.username, f"{prevTransactions}{transactionLogStr}")
    balancesDatabase.insertValue(self.username, self.balance)

  def transferTo(self, target: 'Account', amount: int):
    if target.exists is False:
      raise Exception("target_does_not_exist")
    self.addTransaction(-amount, f"Transfer to {target.username}")
    target.addTransaction(amount, f"Transfer from {self.username}")

  def delete(self, password: str):
    self.validateAccount()
    if self.password != password:
      raise Exception("wrong_password_for_delete")
    self.exists = False
    accountsDatabase.popEntry(self.username)
    transactionsDatabase.popEntry(self.username)
    balancesDatabase.popEntry(self.username)
  
  def changePassword(self, newPass: str):
    self.validateAccount()
    self.password = newPass
    accountsDatabase.insertValue(self.username, newPass)
  
