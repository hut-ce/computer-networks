import socket
import threading


class User:
    def __init__(self, ID, role, connection, address):
        self.roles = ["user", "admin", "manager"]
        self.name = ""
        self.ID = ID
        self.blocked_IDs = []
        if role in self.roles:
            self.role = role
        else:
            self.role = 'user'
        self.connection = connection
        self.address = address
        self.blocked_names = []
        self.is_blocked_by_names = []
        self.is_blocked_by_ID = []

    def block_ID(self, other):
        blocked_ID = other.ID
        if blocked_ID not in self.blocked_IDs:
            self.blocked_IDs.append(blocked_ID)
            print(f"{other.name} is blocked!")
        else:
            print(f"ID '{other.name}' already is blocked! ")

    def unblock_ID(self, other):
        unblocked_ID = other.ID
        if unblocked_ID in self.blocked_IDs:
            self.blocked_IDs.remove(unblocked_ID)
            print(f"unblocked '{other.name}'!")
        else:
            print(f"{other.name} is not blocked")

    def block_name(self, name):
        blocked_name = name
        if blocked_name not in self.blocked_names:
            self.blocked_names.append(blocked_name)
            print(f"{self.name} has blocked {name}!")
        else:
            print(f"{self.name}:'{name}' already is blocked or docent exists! ")

    def unblock_name(self, name):
        unblocked_name = name
        if unblocked_name in self.blocked_names:
            self.blocked_names.remove(unblocked_name)
            print(f"{self.name} unblocked '{name}'!")
        else:
            print(f"{self.name}: {name} is not blocked")

    def set_name(self, name):
        self.name = name

    def promote_and_demote(self, role):
        if role in self.roles:
            self.role = role
        else:
            self.role = 'user'

    def disconnect(self):
        self.connection.send("quit!!!".encode('utf-8'))

    def __str__(self):
        return f"username = {self.name}, userID = {self.ID}, UserRole = {self.role}"


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):

        with cls._lock:

            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Chatroom(metaclass=SingletonMeta):

    def __init__(self):
        self.admin_username_passwords = [("ali", "10234"), ("kia", "m@w3"), ("hi", "test123")]
        self.manager_username_passwords = [("hoom", "234dfd"), ("rez", "sfg@w3"), ("hosseinpoor", "I AM A TA")]
        self.clients = []
        self.connections = []
        self.next_ID = 0

    def find_user_by_name(self, name):
        for c in self.clients:
            if c.name == name:
                return c
        return None

    def logins_handler(self, username, password, client: User):
        if (username, password) in self.admin_username_passwords:
            client.promote_and_demote("admin")
            client.connection.send("successfully logged in as admin".encode('utf-8'))
        if (username, password) in self.manager_username_passwords:
            client.promote_and_demote("manager")
            client.connection.send("successfully logged in as manager".encode('utf-8'))

    def find_next_ID(self):
        _ = self.next_ID
        self.next_ID += 1
        return _

    def add_client(self, client: User):
        self.clients.append(client)
        self.connections.append(client.connection)

    def remove_client(self, client: User):
        self.connections.remove(client.connection)
        self.clients.remove(client)

    def create_clients(self, role, connection, address):
        if connection not in self.connections:
            ID = self.find_next_ID()
            client = User(ID, role, connection, address)
            self.add_client(client)
            return client

        else:
            print("User already exists!")

    def handle_clients(self, connection, address):
        print(f"{address} is attempting to connect to the server!")
        current_client = self.create_clients("user", connection, address)
        try:
            name = connection.recv(1024).decode()
            current_client.set_name(name)
            print(current_client, "has successfully connected to chatroom!")
        except KeyboardInterrupt:
            print(f"Connection with {address} is closed")
        except ConnectionResetError:
            print(f"Connection with {address} was forcibly closed")

        while True:
            try:
                command = connection.recv(1024).decode()
                if not command:
                    break

                if command == "send" or command == "s":
                    message = connection.recv(1024).decode()

                    if not message:
                        break
                    print(f"address: <{address}>| {message}")

                    for c in self.clients:
                        if c != current_client:
                            if c.name not in current_client.blocked_names and c.name not in current_client.is_blocked_by_names:
                                c.connection.send(message.encode('utf-8'))

                elif command == "block" or command == "b":
                    message = connection.recv(1024).decode()
                    if not message:
                        break
                    current_client.block_name(message)
                    blocked_client = self.find_user_by_name(message)
                    if blocked_client:
                        blocked_client.is_blocked_by_names.append(current_client.name)

                elif command == "private message" or command == "pv":
                    message = connection.recv(1024).decode()
                    if not message:
                        break
                    found_user = False
                    for c in self.clients:
                        if c.name == message and c.name not in current_client.blocked_names:
                            found_user = True
                            print(f"user '{c.name}' was found, establishing connection...")
                            message = connection.recv(1024).decode()
                            c.connection.send("pv incoming".encode('utf-8'))
                            c.connection.send(message.encode('utf-8'))
                            print(f"message from {current_client.name} sent to {c.name}")
                            break
                    if not found_user:
                        _ = connection.recv(1024).decode()
                        current_client.connection.send("user not found!".encode('utf-8'))

                elif command == "kick" or command == "k":
                    message = connection.recv(1024).decode()
                    if current_client.role == "admin" or current_client.role == "manager":
                        found_user = False
                        if not message:
                            break
                        for c in self.clients:
                            if c.name == message:
                                found_user = True
                                print(f"user '{c.name}' was found...")
                                c.disconnect()
                                print(f"user {c.name} was kicked out of the chatroom!")
                                current_client.connection.send(f"user {c.name} was kicked out of the chatroom!".encode('utf-8'))
                        if not found_user:
                            print(f"user '{message}' not found!")
                            current_client.connection.send(f"user '{message}' not found!".encode('utf-8'))
                    else:
                        current_client.connection.send("insufficient admin privileges".encode('utf-8'))
                elif command == "login" or command == "l":
                    username = connection.recv(1024).decode()
                    password = connection.recv(1024).decode()
                    self.logins_handler(username, password, current_client)

            except KeyboardInterrupt:
                print(f"Connection with {address} is closed")
                break
            except ConnectionResetError:
                print(f"Connection with {address} was forcibly closed")
                break
            except OSError:
                print("something went wrong!")

        self.remove_client(current_client)
        connection.close()
        print(f"{address} has left the chatroom!")


IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((IP, PORT))

chatroom = Chatroom()

SERVER.listen(10)
print("Server is Running and is waiting for connections...")


try:
    while True:
        connection, address = SERVER.accept()
        thread = threading.Thread(target=chatroom.handle_clients, args=(connection, address))
        thread.start()


except KeyboardInterrupt:
    print("Shutting server down...")
    SERVER.close()
