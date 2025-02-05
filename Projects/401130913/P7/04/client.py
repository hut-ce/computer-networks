import socket
import json

def interact_with_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 7000))

    while True:
        action = input("Enter action (set/get) or 'exit': ")
        if action.lower() == "exit":
            break

        key = input("Enter key: ")
        value = None
        if action.lower() == "set":
            value = input("Enter value: ")

        command = json.dumps({"action": action, "key": key, "value": value})
        client.send(command.encode())
        response = client.recv(1024).decode()
        print(f"Response: {response}")

    client.close()

if __name__ == "__main__":
    interact_with_server()
