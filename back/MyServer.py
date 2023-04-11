from http.server import BaseHTTPRequestHandler
from os import path
from glob import glob
import json
from Account import Account


frontEndDir = path.join(path.dirname(__file__), "..", "front")
frontEndFilePaths = glob(path.join(frontEndDir, "*"))
frontEndFileNames = [path.basename(filePath) for filePath in frontEndFilePaths]
filesMap = {fileName: filePath for fileName, filePath in zip(frontEndFileNames, frontEndFilePaths)}


class MyServer(BaseHTTPRequestHandler):
  
  def respond(self, code: int, headers: dict, content: str):
    self.send_response(code)
    for key, value in headers.items():
      self.send_header(key, value)
    self.end_headers()
    self.wfile.write(content.encode('utf-8'))

  def readFile(self, filePath: str):
    with open(filePath, 'r') as file:
      return file.read()

  def getStrippedPath(self):
    return self.path[1:].split("?")[0]
  
  def getQueryParams(self):
    return self.path.split("?")[1].split("&")
  
  def getPostContent(self):
    return self.rfile.read(int(self.headers.get("Content-Length"))).decode('utf-8')

  def sendNotFound(self):
    self.respond(404, {}, "<h1>404 Not Found</h1>")
  
  def sendUnauthorized(self, jsonMsg):
    self.respond(401, {"WWW-Authenticate": "Basic realm=\"Login Required\""}, f'''{{}}''')

  def do_GET(self):
    if self.getStrippedPath() == '':
      self.respond(200, {"Content-type": "text/html"}, self.readFile(filesMap['index.html']))
    elif self.getStrippedPath() in filesMap:
      self.respond(200, {"Content-type": "text/html"}, self.readFile(filesMap[self.getStrippedPath()]))
    else:
      self.respond(404, {}, "<h1>404 Not Found</h1>")
  
  def do_POST(self):
    dataRecieved = json.loads(self.getPostContent())
    action = dataRecieved['action']
    username = dataRecieved['data']['bank-ass-username']
    password = dataRecieved['data']['bank-ass-password']
    
    if action == "login":
      account = Account(username, password)
      if not account.isSaved():
        pass
        

    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes('''{"aaa": "bb"}''', 'utf-8'))
