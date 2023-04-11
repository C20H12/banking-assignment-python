from MyServer import MyServer
from http.server import HTTPServer


webServer = HTTPServer(("localhost", 8080), MyServer)
print("started")

try:
  webServer.serve_forever()
except KeyboardInterrupt:
  webServer.server_close()
  print("server closed")
