import socket
import threading

clients = {}
blocked_users = {}
user_roles = {}  # ذخیره نقش‌های کاربران
lock = threading.Lock()

def handle_client(CONNECTION, ADDR):
    print(f"Connected to {ADDR}")

    username = CONNECTION.recv(1024).decode('utf-8')
    
    with lock:
        clients[username] = CONNECTION
        blocked_users[username] = []
        user_roles[username] = 'user'  # پیش‌فرض نقش کاربران عادی است
    
    print(f"{username} joined the chat.")
    
    # دریافت نقش از کاربر (مدیر، ناظر، کاربر عادی)
    role = CONNECTION.recv(1024).decode('utf-8')
    if role in ['admin', 'moderator', 'user']:
        with lock:
            user_roles[username] = role
    else:
        # در صورتی که نقش معتبر نباشد، به عنوان کاربر عادی در نظر گرفته می‌شود
        with lock:
            user_roles[username] = 'user'
    
    while True:
        Message = CONNECTION.recv(1024).decode('utf-8')
        if not Message:
            print(f"Connection with {ADDR} is closed")
            break

        if Message.startswith('@'):
            target_user, private_message = Message[1:].split(" ", 1)
            
            with lock:
                if target_user in clients:
                    if target_user in blocked_users and username in blocked_users[target_user]:
                        CONNECTION.send(f"You have been blocked by {target_user}, you cannot send messages to them.".encode('utf-8'))
                    elif username in blocked_users and target_user in blocked_users[username]:
                        CONNECTION.send(f"You have blocked {target_user}, you cannot send messages to them.".encode('utf-8'))
                    else:
                        clients[target_user].send(f"Private message from {username}: {private_message}".encode('utf-8'))
                else:
                    CONNECTION.send(f"User {target_user} not found.".encode('utf-8'))
        elif Message.lower().startswith('block'):
            target_user = Message.split(' ')[1]
            response = block_user(username, target_user)
            CONNECTION.send(response.encode('utf-8'))
        elif Message.lower().startswith('unblock'):
            target_user = Message.split(' ')[1]
            response = unblock_user(username, target_user)
            CONNECTION.send(response.encode('utf-8'))
        else:
            broadcast(Message, CONNECTION, username)
    
    with lock:
        del clients[username]
        del blocked_users[username]
        del user_roles[username]
    CONNECTION.close()

def broadcast(Message, CONNECTION, username):
    with lock:
        for client in clients.values():
            if client != CONNECTION:
                try:
                    client.send(f"{username}: {Message}".encode('utf-8'))
                except:
                    continue

def block_user(username, target_user):
    with lock:
        if user_roles[username] not in ['admin', 'moderator']:
            return "You do not have permission to block users."
        
        if target_user not in blocked_users[username]:
            blocked_users[username].append(target_user)
            return f"You have successfully blocked {target_user}."
        else:
            return f"{target_user} is already blocked."

def unblock_user(username, target_user):
    with lock:
        if user_roles[username] not in ['admin', 'moderator']:
            return "You do not have permission to unblock users."
        
        if target_user in blocked_users[username]:
            blocked_users[username].remove(target_user)
            return f"You have successfully unblocked {target_user}."
        else:
            return f"{target_user} is not in your block list."

def main():
    IP = socket.gethostbyname(socket.gethostname())
    Port = 5050

    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server.bind((IP , Port))
    Server.listen()

    print("Server is Running!")

    while True:
        CONNECTION , ADDR = Server.accept()
        thread = threading.Thread(target=handle_client , args=(CONNECTION , ADDR))
        thread.start()

if __name__ == "__main__":
    main()
