from SimpleDatabase import SimpleDb
from uuid import uuid4

accountsDatabase = SimpleDb("accounts.txt")
transactionsDatabase = SimpleDb("transactions.txt")
tokensDatabase = SimpleDb("tokens.txt")

class Account:
  def __init__(self, username: str, password: str):
    self.username = username
    self.password = password
    self.balance = 100
    self.authenticated = False

  @staticmethod
  def fromToken(token):
    username = tokensDatabase.getValue(token)
    if username is None:
      return None
    accountAssociated = Account(username, "")
    accountAssociated.authenticated = True
    return accountAssociated

  def isSaved(self):
    return accountsDatabase.getValue(self.username) is not None

  def save(self):
    return accountsDatabase.insertValue(self.username, self.password)
  
  def authenticate(self):
    if accountsDatabase.getValue(self.username) == self.password:
      self.authenticated = True
      sessionToken = uuid4().hex()
      tokensDatabase.insertValue(sessionToken, self.username)
      return sessionToken
    return None
  
  def getTransactions(self):
    if not self.authenticated:
      return "not_authenticated"
    return transactionsDatabase.getValue(self.username)
  
  def addTransaction(self, amount: int):
    if not self.authenticated:
      return "not_authenticated"
    self.balance += amount
    transactionsDatabase.insertValue(self.username, f"{self.getTransactions()},{amount}")
  
  def delete(self):
    if not self.authenticated:
      return "not_authenticated"
    accountsDatabase.popEntry(self.username)
    transactionsDatabase.popEntry(self.username)
    tokensDatabase.popEntry(self.username)
  
  def changePassword(self, newPass):
    if not self.authenticated:
      return "not_authenticated"
    accountsDatabase.insertValue(self.username, newPass)