from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer


def main():    
    auth = DummyAuthorizer()
    auth.add_user("auth", "yas83", ".", perm="elradfmw")  
    auth.add_anonymous(".")  
    handler = FTPHandler
    handler.authorizer = auth
    server = FTPServer(("127.0.0.1", 21), handler)
    print("server is running on 127.0.0.1:21")
    server.serve_forever()

if __name__ == "__main__":
    main()