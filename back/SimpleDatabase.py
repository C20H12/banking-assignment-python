from os import path
from typing import Optional

class SimpleDb:
  def __init__(self, fileName: str):
    self.filePath = path.join(path.dirname(__file__), fileName)

  def getValue(self, key: str) -> Optional[str]:
    with open(self.filePath, "r") as file:
      fileLines = file.read().splitlines()
    for line in fileLines:
      k, v = line.split(" <<separator>> ")
      if k == key:
        return v
    return None

  def popEntry(self, key: str) -> Optional[str]:
    with open(self.filePath, "r") as file:
      fileLines = file.read().splitlines()
    removedValue = None
    with open(self.filePath, "w") as file:
      for line in fileLines:
        k, v = line.split(" <<separator>> ")
        if k == key:
          removedValue = v
        else:
          file.write(line + '\n')
    return removedValue

  def insertValue(self, key: str, value) -> bool:
    try:
      self.popEntry(key)
      with open(self.filePath, "a+") as file:
        file.write(f"{key} <<separator>> {value}\n")
    except:
      return False
    return True
  
