import socket

def start_client():
    ip = "127.0.0.1"  
    port = 5353       

    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    print("[CONNECTED] Connected to DNS server.")

    try:
        while True:
            
            domain_name = input("Enter domain name (or 'exit' to quit): ")
            if domain_name.lower() == "exit":
                break
            
            
            client_socket.send(domain_name.encode())

            
            response = client_socket.recv(1024).decode()
            print(f"[RESPONSE] {response}")
    except:
        print("[ERROR] Connection lost.")
    finally:
        client_socket.close()
        print("[DISCONNECTED] Client disconnected.")

if __name__ == "__main__":
    start_client()
