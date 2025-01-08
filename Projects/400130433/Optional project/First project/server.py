from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from threading import Thread



def start_ftp_server():
    
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "password", ".", perm="elradfmw")  
    authorizer.add_anonymous(".")  

    
    handler = FTPHandler
    handler.authorizer = authorizer

    
    server = FTPServer(("127.0.0.1", 2121), handler)
    print("FTP server is running on 127.0.0.1:2121")
    server.serve_forever()