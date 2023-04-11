from SimpleDatabase import SimpleDb
db = SimpleDb("data_files/test_db.txt")


db.insertValue("k1", 000)
for i in range(20):
  db.insertValue("k"+str(i), i)

db.popEntry("k1")

print(db.getValue("k2"))
print(db.getValue("k3"))
print(db.getValue("k4"))

print(db.getValue("k4"))

print(db.getValue("k12"))

print(db.getValue("k22"))
print(db.getValue("k25"))
print(db.getValue("k26"))

db.insertValue('k12', 'new')