import socket
import time
import random


MODE = "NORMAL"  

def send_requests():

    ip = '127.0.0.1'  
    port = 8080       
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    
    try:
        while True:
            
            if MODE == "NORMAL":
                
                time.sleep(random.uniform(0.5, 2))  
            elif MODE == "DDOS":
               
                time.sleep(0.1)
            
            client.send("Hello, Server!".encode())
            response = client.recv(1024).decode()
            print(f"Server Response: {response}")
            
            if "blocked" in response.lower():
                print("You have been blocked!")
                break
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        client.close()

if __name__ == "__main__":
    send_requests()
