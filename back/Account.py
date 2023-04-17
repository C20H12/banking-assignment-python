from SimpleDatabase import SimpleDb
from datetime import datetime
from json import dumps as JSON_stringify, loads as JSON_parse


# TODO: add false for isTesting
testing = True
# key is username, value is password
accountsDatabase = SimpleDb("data_files/accounts.txt", testing)
# key is username, value is balance
balancesDatabase = SimpleDb("data_files/balances.txt", testing)
# key is username, value is the JSON data for transactions
transactionsDatabase = SimpleDb("data_files/transactions.txt", testing)


class AccountError(Exception):
  '''
  An exception that is raised when an account operation fails
  Contains a message that can be sent to the front end
  '''
  pass


class Account:
  '''
  Represents an user's account
  Contains methods for doing operations on this account
  '''

  def __init__(self, username: str, password: str = '', asTransferTarget: bool = False):
    self.username = username
    self.password = password
    dataBaseEntry = accountsDatabase.getValue(self.username)
    self.exists = dataBaseEntry is not None
    self.authenticated = False
    self.balance = 0

    # if the account do not exist, can't authenticate or get the balance
    # aborts the creation
    if not self.exists:
      return
    
    self.authenticated = dataBaseEntry == self.password
    
    # temporarily authenticate the account if it is a transfer target
    if not self.authenticated and asTransferTarget:
        self.authenticated = True

    # get the balance from the database, giving it a default value of 100
    self.balance = float(balancesDatabase.getValue(self.username) or 100)
  
  
  # Validation methods
  # These will raise an error to abort from the function if the checks fail
  def _validateAccount(self):
    if self.exists is False:
      raise AccountError("Account does not exist")
    if self.authenticated is False:
      raise AccountError("Not authenticated")

  def _validateTransaction(self, amount):
    self._validateAccount()
    if self.balance < -amount:
      raise AccountError("Not enough funds")
    if amount == 0:
      raise AccountError("Zero amount")
  
  

  # Account operations  
  def saveAccount(self):
    '''
    Register
    Saves this account to the database
    Added the initial 100 to the transac log
    '''
    self.exists = True
    self.authenticated = True
    accountsDatabase.insertValue(self.username, self.password)
    self.addTransaction(100, "initial balance, the benevolence")
  
  def getTransactions(self) -> list:
    '''
    Get the transac logs for this account from the database
    The logs are stored as a JSON list of objects
    Returns a list of the objects containing details about the transaction
    '''
    self._validateAccount()
    transactions =  transactionsDatabase.getValue(self.username)
    if transactions == None:
      return []
    return JSON_parse(f"{transactions}")
    
  
  def addTransaction(self, amount: int, reason: str):
    '''
    Add a transaction to the transac log
    Updates the databese for the balance and transactions 
    '''
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
    '''
    Transfer money to another account
    Aborts if the target does not exist in the database
    Aborts if the target's username is same as self's
    Adds a transaction on this account and the target account
    '''
    self._validateAccount()
    if target.exists is False:
      raise AccountError("Target does not exist")
    if target.username == self.username:
      raise AccountError("Can't transfer to self")
    self.addTransaction(-amount, f"Transfer to {target.username}")
    target.addTransaction(amount, f"Transfer from {self.username}")

  def delete(self, confirmPassword: str):
    '''
    Delete this account
    Aborts if the confirm password is incorrect
    Removes the account from the databases
    '''
    self._validateAccount()
    if self.password != confirmPassword:
      raise AccountError("Incorrect password")
    self.exists = False
    accountsDatabase.popEntry(self.username)
    transactionsDatabase.popEntry(self.username)
    balancesDatabase.popEntry(self.username)
  
  def changePassword(self, newPass: str):
    '''
    Change the password of this account
    Updates the password in the database
    '''
    self._validateAccount()
    self.password = newPass
    accountsDatabase.insertValue(self.username, newPass)
  
