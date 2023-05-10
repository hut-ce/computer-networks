import socket
def get_remote_machine_info():
    remote_host = 'www.python.org'
    try:
        print( "IP address: %s" %socket.gethostbyname(remote_host))
    
    except socket.error:
        print (f"{remote_host}: {socket.error}")


if __name__ == '__main__':
    get_remote_machine_info()