from MyServer import MyServer
from http.server import HTTPServer
from os import path

url = "localhost"
if path.exists(path.join(path.dirname(__file__), '..', '.replit')):
  url = "0.0.0.0"


webServer = HTTPServer((url, 8080), MyServer)
print("started")

try:
  webServer.serve_forever()
except KeyboardInterrupt:
  webServer.server_close()
  print("server closed")
