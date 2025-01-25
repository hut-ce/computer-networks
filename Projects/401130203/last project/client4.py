import socket

def start_client(host="127.0.0.1", port=65432):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"Connected to server {host}:{port}")

    try:
        while True:
            command = input("Enter command (SET/GET/DELETE/EXIT): ").strip()
            client.send(command.encode('utf-8'))

            response = client.recv(1024).decode('utf-8')
            print(f"Server: {response}")

            if command.upper() == "EXIT":
                break

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()

if __name__ == "__main__":
    start_client()
