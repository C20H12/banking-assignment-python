from Account import Account, AccountError
from glob import glob
from http.server import BaseHTTPRequestHandler
from json import dumps as JSON_stringify, loads as JSON_parse
from mimetypes import guess_type
from os import path
from typing import Union


frontEndDir = path.join(path.dirname(__file__), "..", "front")
frontEndFilePaths = glob(path.join(frontEndDir, "*"))
frontEndFileNames = [path.basename(filePath) for filePath in frontEndFilePaths]
filesMap = {fileName: filePath for fileName, filePath in zip(frontEndFileNames, frontEndFilePaths)}


class MyServer(BaseHTTPRequestHandler):
  
  # helper methods
  def readFile(self, filePath: str):
    '''
    Reads a file and returns its content as bytes
    '''
    with open(filePath, 'rb') as file:
      return file.read()

  def getStrippedPath(self):
    '''
    Returns the path without the first slash and without the query string
    '''
    return self.path[1:].split("?")[0]
  
  def getPostContent(self):
    '''
    Returns the *full* content of the POST request as a string
    '''
    return self.rfile.read(int(self.headers.get("Content-Length"))).decode('utf-8')
  
  def sanitizeInput(self, inputStr: str):
    '''
    Sanitizes the input string to prevent XSS
    Also prevents it from messing with the database since it uses these <>s in the separator
    '''
    return inputStr.replace("<", "&lt;").replace(">", "&gt;")
  

  # responding methods
  def respond(self, code: int, headers: dict, content: Union[bytes, str]):
    '''
    Sends a response to the client
    '''
    self.send_response(code)
    # send the headers
    for key, value in headers.items():
      self.send_header(key, value)
    self.end_headers()
    # converts the contents to bytes since it can only send bytes
    if type(content) is str:
      self.wfile.write(content.encode("utf-8"))
    else:
      self.wfile.write(content)

  def sendNotFound(self):
    '''Sends a 404 Not Found response as html'''
    self.respond(404, {"Content-type": "text/html"}, "<h1>404 Not Found</h1>")
  
  def sendUnauthorized(self, msg: str):
    '''Sends a 401 Unauthorized response as json with a message'''
    self.respond(
      401, 
      {"Authorization": "BasicCustom", "Content-type": "text/json"}, 
      JSON_stringify({"message": msg})
    )

  def sendForbidden(self):
    '''Sends a 403 Forbidden response as json with a message'''
    self.respond(403, {"Content-type": "text/json"}, JSON_stringify({"message": "Do not POST here"}))
  
  def sendSuccess(self, msg: str, data=[]):
    '''Sends a 200 OK response as json with a message and optional data'''
    self.respond(200, {"Content-type": "text/json"}, JSON_stringify({"message": msg, "data": data}))

  def sendError(self, msg: str):
    '''Sends a 500 Internal Server Error response as json with a message'''
    self.respond(500, {"Content-type": "text/json"}, JSON_stringify({"message": msg}))


  # listening methods
  def do_GET(self):
    '''Fires when a GET request is recieved'''
    # serve the index.html file if the path is empty
    if self.getStrippedPath() == '':
      self.respond(200, {"Content-type": "text/html"}, self.readFile(filesMap['index.html']))
    # serve the file if it exists
    elif self.getStrippedPath() in filesMap:
      fileToServe = filesMap[self.getStrippedPath()]
      contentType, _ = guess_type(fileToServe)
      self.respond(200, {"Content-type": contentType}, self.readFile(fileToServe))
    # send a 404 response
    else:
      self.sendNotFound()
  
  def do_POST(self):
    '''Fires when a POST request is recieved'''

    # only allow POST requests to the /account path
    if self.getStrippedPath() != 'account':
      self.sendForbidden()
      return
    
    # parse the request body
    recieved = JSON_parse(self.getPostContent())
    action = recieved['action']
    data = recieved['data']
    accountInfo = recieved['accountInfo']

    # create an account object for the current user
    account = Account(
      self.sanitizeInput(accountInfo['username']), self.sanitizeInput(accountInfo['password'])
    )

    # handle the request according to the action to perform
    # if an actions fails, send an error response
    # if the action succeeded, send a success response with the transactions data
    try:
      if action == "login":
        if not account.exists:
          self.sendUnauthorized("Account does not exist, register first")
          return
        if not account.authenticated:
          self.sendUnauthorized("Wrong password")
          return
        self.sendSuccess("Succesfully logged in", account.getTransactions())

      elif action == "register":
        if account.exists:
          self.sendUnauthorized("Account already exists")
          return
        account.saveAccount()
        self.sendSuccess("Account created")
    
      elif action == "deposit":
        account.addTransaction(float(data['deposit-amount']), "Deposit")
        self.sendSuccess("Deposit succesful", account.getTransactions())
      
      elif action == "withdraw":
        account.addTransaction(-float(data['withdraw-amount']), "Withdraw")
        self.sendSuccess("Withdraw succesful", account.getTransactions())
      
      elif action == "transfer":
        account.transferTo(
          Account(self.sanitizeInput(data['transfer-target']), asTransferTarget=True), 
          float(data['transfer-amount'])
        )
        self.sendSuccess("Transfer succesful", account.getTransactions())

      elif action == "change-pass":
        account.changePassword(data['change-password-new'])
        self.sendSuccess("Password changed, now log in again", account.getTransactions())
      
      elif action == "delete":
        account.delete(data['delete-password-confirm'])
        self.sendSuccess("Account deleted")

      elif action == "refresh":
        self.sendSuccess("Refresh succesful", account.getTransactions())

      # logout is handled by the front end

      else:
        self.sendUnauthorized("Invalid action")

    except AccountError as ae:
      # if there is an error with account operations, ie. aborted, 
      # send a 401 and the message
      self.sendUnauthorized(f"Account Error: {ae}")
      return
    
    except Exception as ex:
      # if there is some other error, send a 500 and the error text as message
      print(ex)
      self.sendError(f"Internal Error: {ex}")