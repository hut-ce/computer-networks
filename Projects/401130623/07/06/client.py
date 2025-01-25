import socket
import time
import random
MODE = "nor"  
def req():      
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1' , 100))
    try:
        while True:
            if MODE == "nor":
                time.sleep(random.uniform(0.5, 2))  
            elif MODE == "ddos":
                time.sleep(0.1)
            client.send("Message".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(f"Server Response: {response}")
            if "blocked" in response.lower():
                print("You've been blocked!")
                break
    except Exception as error:
        print(f"Error: {error}")
    finally:
        client.close()
if __name__ == "__main__":
    req()
