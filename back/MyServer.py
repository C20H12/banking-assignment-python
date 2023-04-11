from http.server import BaseHTTPRequestHandler
from os import path
from glob import glob


frontEndDir = path.join(path.dirname(__file__), "..", "front")
frontEndFilePaths = glob(path.join(frontEndDir, "*"))
frontEndFileNames = [path.basename(filePath) for filePath in frontEndFilePaths]
filesMap = {fileName: filePath for fileName, filePath in zip(frontEndFileNames, frontEndFilePaths)}


class MyServer(BaseHTTPRequestHandler):

  def write_response(self, content: str):
    return self.wfile.write(bytes(content, 'utf-8'))
  
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
    return self.rfile.read(int(self.headers.get("Content-Length")))

  def do_GET(self):
    if self.path == '/':
      self.respond(200, {"Content-type": "text/html"}, self.readFile(filesMap['index.html']))
    elif self.getStrippedPath() in filesMap:
      self.respond(200, {"Content-type": "text/html"}, self.readFile(filesMap[self.getStrippedPath()]))
    else:
      self.respond(404, {}, "<h1>404 Not Found</h1>")
  
  def do_POST(self):
    print("post", self.rfile.read(int(self.headers.get("Content-Length"))))
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes('''{"aaa": "bb"}''', 'utf-8'))
