import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
Port = 5050

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Client.connect((IP, Port))

def listen_for_messages():
    while True:
        try:
            Message = Client.recv(1024).decode('utf-8')
            if Message:
                print(f"\n{Message}")
            else:
                print("Server connection closed.")
                break
        except:
            print("Error")
            break

thread = threading.Thread(target=listen_for_messages)
thread.daemon = True  # اگر برنامه اصلی بسته شد
thread.start()

username = input("Enter your username:\n")
Client.send(username.encode('utf-8'))

# انتخاب نقش کاربر
role = input("Enter your role (admin, moderator, or user):\n")
Client.send(role.encode('utf-8'))

while True:
    Message = input("Enter your message (use @username for private message, 'block <username>' to block, 'unblock <username>' to unblock):\n")
    
    if Message.lower() == 'exit':
        print("Disconnecting from the server...")
        Client.send("User has left the chat.".encode('utf-8'))
        Client.close()
        break
    elif Message.lower().startswith('block'):
        target_user = Message.split(' ')[1]
        Client.send(f"block {target_user}".encode('utf-8'))
    elif Message.lower().startswith('unblock'):
        target_user = Message.split(' ')[1]
        Client.send(f"unblock {target_user}".encode('utf-8'))
    else:
        Client.send(Message.encode('utf-8'))
