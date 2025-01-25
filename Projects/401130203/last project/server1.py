from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
def do_something():
    auth = DummyAuthorizer()
    auth.add_user("u1", "pass1", "/path/to/share", perm="elradfmw")
    auth.add_user("u2", "pass2", "/path/to/share", perm="elr")
    h = FTPHandler
    h.authorizer = auth
    s = FTPServer(("0.0.0.0", 2121), h)
    print("server is running")
    s.serve_forever()
do_something()
