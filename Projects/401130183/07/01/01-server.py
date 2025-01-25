from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user("user", "12345", "./ftp_files", perm="elradfmw")
authorizer.add_anonymous("./ftp_files")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("0.0.0.0", 2121), handler)
server.serve_forever()
