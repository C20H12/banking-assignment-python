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
  
  def respond(self, code: int, headers: dict, content: Union[bytes, str]):
    self.send_response(code)
    for key, value in headers.items():
      self.send_header(key, value)
    self.end_headers()
    if type(content) is str:
      self.wfile.write(content.encode("utf-8"))
    else:
      self.wfile.write(content)

  def readFile(self, filePath: str):
    with open(filePath, 'rb') as file:
      return file.read()

  def getStrippedPath(self):
    return self.path[1:].split("?")[0]
  
  def getPostContent(self):
    return self.rfile.read(int(self.headers.get("Content-Length"))).decode('utf-8')

  def sendNotFound(self):
    self.respond(404, {"Content-type": "text/html"}, "<h1>404 Not Found</h1>")
  
  def sendUnauthorized(self, msg: str):
    self.respond(
      401, 
      {"Authorization": "BasicCustom", "Content-type": "text/json"}, 
      JSON_stringify({"message": msg})
    )

  def sendForbidden(self):
    self.respond(403, {"Content-type": "text/json"}, JSON_stringify({"message": "Do not POST here"}))
  
  def sendSuccess(self, msg: str, data=[]):
    self.respond(200, {"Content-type": "text/json"}, JSON_stringify({"message": msg, "data": data}))

  def do_GET(self):
    if self.getStrippedPath() == '':
      self.respond(200, {"Content-type": "text/html"}, self.readFile(filesMap['index.html']))
    elif self.getStrippedPath() in filesMap:
      fileToServe = filesMap[self.getStrippedPath()]
      contentType, _ = guess_type(fileToServe)
      self.respond(200, {"Content-type": contentType}, self.readFile(fileToServe))
    else:
      self.sendNotFound()
  
  def do_POST(self):
    if self.getStrippedPath() != 'account':
      self.sendForbidden()
      return
    
    recieved = JSON_parse(self.getPostContent())
    action = recieved['action']
    data = recieved['data']
    accountInfo = recieved['accountInfo']

    account = Account(accountInfo['username'], accountInfo['password'])

    if action == "login":
      if not account.exists:
        self.sendUnauthorized("Account does not exist, register first")
        return
      if not account.authenticated:
        self.sendUnauthorized("Wrong password")
        return
      self.sendSuccess("Succesfully logged in", account.getTransactions())

    if action == "register":
      if account.exists:
        self.sendUnauthorized("Account already exists, go login")
        return
      account.saveAccount()
      self.sendSuccess("Account created")
    
    try:
      if action == "deposit":
        account.addTransaction(float(data['deposit-amount']), "Deposit")
        self.sendSuccess("Deposit succesful", account.getTransactions())
      
      if action == "withdraw":
        account.addTransaction(-float(data['withdraw-amount']), "Withdraw")
        self.sendSuccess("Withdraw succesful", account.getTransactions())
      
      if action == "transfer":
        account.transferTo(Account(data['transfer-target'], asTransferTarget=True), float(data['transfer-amount']))
        self.sendSuccess("Transfer succesful", account.getTransactions())

      if action == "logout":
        self.sendSuccess("Logged out")

      if action == "change-pass":
        account.changePassword(data['change-password-new'])
        self.sendSuccess("Password changed")
      
      if action == "delete":
        account.delete(data['delete-password-confirm'])
        self.sendSuccess("Account deleted")
    
    except AccountError as ae:
      self.sendUnauthorized(f"Account Error: {ae}")
      return
    
    except Exception as ex:
      self.respond(500, {"Content-type": "text/json"}, f"Internal server error: {ex}")