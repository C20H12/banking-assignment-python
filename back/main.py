from MyServer import MyServer
from http.server import HTTPServer
from os import path

# the url the server runs at
url = "localhost"

# check if running on repl.it, setting url to
# this makes the output panel show on replit
if path.exists(path.join(path.dirname(__file__), '..', '.replit')):
  url = "0.0.0.0"

# create a new server 
webServer = HTTPServer((url, 8080), MyServer)

print("started")

# start the server
# run until keyboard interrupt
try:
  webServer.serve_forever()
except KeyboardInterrupt:
  webServer.server_close()
  print("server closed")
