from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from threading import Thread



def start_ftp_server():

    Dumm_authoriz = DummyAuthorizer()
    Dumm_authoriz.add_user("user", "password", ".", perm="elradfmw")  
    Dumm_authoriz.add_anonymous(".")  

    
    Handle = FTPHandler
    Handle.authorizer = Dumm_authoriz

    
    server = FTPServer(("127.0.0.1", 2121), Handle)
    print("FTP server is running on 127.0.0.1:2121")
    server.serve_forever()