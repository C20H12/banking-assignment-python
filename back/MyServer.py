from Account import Account
from glob import glob
from http.server import BaseHTTPRequestHandler
import json
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
  
  def sendUnauthorized(self, jsonMsg: str):
    self.respond(
      401, 
      {"Authorization": "BasicCustom",
       "Content-type": "text/json"}, 
      jsonMsg
    )

  def sendForbidden(self):
    self.respond(403, {"Content-type": "text/json"}, '''{"message": "do not POST to here"}''')
  
  def sendSuccess(self, jsonMsg: str):
    self.respond(200, {"Content-type": "text/json"}, jsonMsg)

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
    
    recieved = json.loads(self.getPostContent())
    action = recieved['action']
    data = recieved['data']
    accountInfo = recieved['accountInfo']

    account = Account(accountInfo['username'], accountInfo['password'])

    if action == "login":
      if not account.exists:
        self.sendUnauthorized('''{"message": "Account does not exist, register first"}''')
        return
      if not account.authenticated:
        self.sendUnauthorized('''{"message": "Wrong password"}''')
        return
      self.sendSuccess(f'''{{"message": "Succesfully logged in", "data": [{account.getTransactions() or ''}]}}''')

    if action == "register":
      if account.exists:
        self.sendUnauthorized('''{"message": "Account already exists, go login"}''')
        return
      account.saveAccount()
      self.sendSuccess('''{"message": "Account created"}''')
    
    if action == "deposit":
      pass
    


