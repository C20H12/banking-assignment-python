from os import path
from typing import Optional

class SimpleDb:
  '''
  A simple database that stores data in a file
  Data will be stored as a map of string to string
  '''

  def __init__(self, fileName: str, testing=True):
    # get the absolute path of the file to store data in
    self.filePath = path.join(path.dirname(__file__), fileName)

    # create the file if it doesn't exist, or if testing, clears the file
    if not path.exists(self.filePath) or testing:
      with open(self.filePath, "w") as file:
        file.write("")


  def getValue(self, key: str) -> Optional[str]:
    '''
    Gets the value of a key by searching the file's lines
    Returns None if the key doesn't exist
    '''
    with open(self.filePath, "r") as file:
      fileLines = file.read().splitlines()
    for line in fileLines:
      k, v = line.split(" <<separator>> ")
      if k == key:
        return v
    return None

  def popEntry(self, key: str) -> Optional[str]:
    '''
    Removes the entry with the specified key
    Returns the value of the entry if it exists, None if it doesn't
    '''
    with open(self.filePath, "r") as file:
      fileLines = file.read().splitlines()
    removedValue = None
    with open(self.filePath, "w") as file:
      for line in fileLines:
        k, v = line.split(" <<separator>> ")
        if k == key:
          # if the key is found, set the removedValue to the value
          removedValue = v
        else:
          # if the key isn't found, write the line back to the file
          file.write(line + '\n')
    
    return removedValue

  def insertValue(self, key: str, value) -> bool:
    '''
    Inserts a value into the database
    Updates the value if the key already exists
    Returns True if the value was inserted, False if it wasn't
    '''
    try:
      self.popEntry(key)
      with open(self.filePath, "a+") as file:
        file.write(f"{key} <<separator>> {value}\n")
    except:
      return False
    return True
  
