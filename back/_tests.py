'''
tests file
nothing important here
'''

def db_test():
  from SimpleDatabase import SimpleDb
  db = SimpleDb("data_files/test_db.txt")

  # insert
  db.insertValue("k1", 000)
  for i in range(20):
    db.insertValue("k"+str(i), i)

  # remove
  db.popEntry("k1")

  # read
  print(db.getValue("k2"))
  print(db.getValue("k3"))
  print(db.getValue("k4"))

  print(db.getValue("k4"))

  print(db.getValue("k12"))

  print(db.getValue("k22"))
  print(db.getValue("k25"))
  print(db.getValue("k26"))

  # insert an existing key, replacing
  db.insertValue('k12', 'new')


def account_test():
  from Account import Account

  bob = Account("bob", "123")
  print(bob.exists, "does not exist")
  bob.saveAccount()
  print(bob.exists, "exists")

  print(bob.getTransactions(), "none")
  
  wrongPassBob = Account("bob", "1234")
  print(wrongPassBob.authenticated, "not auth'ed")
  

  bob.addTransaction(999, "test")
  print(bob.getTransactions())

  # bob got garbage collected
  del bob

  bobAgain = Account("bob", "123")
  print(bobAgain.exists, "exists")
  print(bobAgain.authenticated, 'is auth')
  print(bobAgain.balance, "should be 1099")

  bobAgain.addTransaction(888, 'test2')
  print(bobAgain.getTransactions())

  try:
    bobAgain.transferTo(Account("null", "null"), 1)
  except Exception as ex:
    print(ex, "worked")
  
  chad = Account("chad", "abc")
  chad.saveAccount()

  bobAgain.transferTo(Account("chad", asTransferTarget=True), 1888)

  print(bobAgain.getTransactions(), "bob log")
  print(chad.getTransactions(), 'chad log')

  bobAgain.changePassword("bob_12345")
  print(bobAgain.password, "bob_12345")

  del bobAgain

  bobOnceMore = Account("bob", "bob_12345")
  print(bobOnceMore.exists, "exists")
  print(bobOnceMore.authenticated, 'is auth')
  print(bobOnceMore.balance, "should be 99")

  bobOnceMore.delete("bob_12345")
  

account_test()