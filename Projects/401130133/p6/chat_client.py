import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext


def caesar_cipher_encode(text, shift):
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char
    return result


def caesar_cipher_decode(text, shift):
    return caesar_cipher_encode(text, -shift)


def check_for_profanity(message):
    PROFANITY_WORDS = [
        'suck', 'stupid', 'pimp', 'dumb', 'homo', 'slut', 'damn', 'ass', 'rape', 'poop', 'cock',
        'crap', 'sex', 'nazi', 'neo-nazi', 'fuck', 'bitch', 'pussy', 'penis', 'vagina', 'whore',
        'shit', 'nigger', 'nigga', 'cocksucker', 'motherfucker', 'wanker', 'cunt', 'faggot', 'fags',
        'asshole', 'piss', 'cum'
    ]
    for word in PROFANITY_WORDS:
        message = message.replace(word, "***")
    return message


# Function to handle receiving messages
def receive_messages(client, chat_box):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            if message == "quit!!!":
                messagebox.showinfo("Info", "Server has disconnected.")
                client.close()
                break
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, f"{message}\n")
            chat_box.config(state=tk.DISABLED)
        except ConnectionError:
            messagebox.showerror("Error", "Lost connection to the server.")
            break


# Send a public message
def send_message(client, entry, name, chat_box):
    message = entry.get()
    if message.strip():
        message = check_for_profanity(message)
        client.send(f"{name}: {message}".encode('utf-8'))
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"You: {message}\n")
        chat_box.config(state=tk.DISABLED)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Message cannot be empty!")


# Send a private message
def send_private_message(client, recipient_entry, message_entry, shift_entry, name, chat_box):
    recipient = recipient_entry.get().strip()
    message = message_entry.get().strip()
    shift = shift_entry.get().strip()

    if not recipient or not message or not shift.isdigit():
        messagebox.showwarning("Warning", "All fields must be filled correctly!")
        return

    encrypted_message = caesar_cipher_encode(message, int(shift))
    client.send(f"private {recipient} {encrypted_message}".encode('utf-8'))
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"Private to {recipient}: {message}\n")
    chat_box.config(state=tk.DISABLED)

    recipient_entry.delete(0, tk.END)
    message_entry.delete(0, tk.END)
    shift_entry.delete(0, tk.END)


# Block a user
def block_user(client, block_entry):
    blocked_name = block_entry.get().strip()
    if blocked_name:
        client.send(f"block {blocked_name}".encode('utf-8'))
        block_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a username to block!")


# Login
def login(client, username_entry, password_entry):
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username and password:
        client.send(f"login {username} {password}".encode('utf-8'))
    else:
        messagebox.showwarning("Warning", "Username and password cannot be empty!")


# GUI Setup
def setup_gui(client, name):
    root = tk.Tk()
    root.title("Chat Client")

    chat_box = scrolledtext.ScrolledText(root, width=50, height=20, state=tk.DISABLED)
    chat_box.pack(padx=10, pady=10)

    message_frame = tk.Frame(root)
    message_frame.pack(pady=5)

    message_entry = tk.Entry(message_frame, width=40)
    message_entry.grid(row=0, column=0, padx=5)

    send_button = tk.Button(message_frame, text="Send", command=lambda: send_message(client, message_entry, name, chat_box))
    send_button.grid(row=0, column=1, padx=5)

    tk.Label(root, text="Private Message").pack(pady=5)
    recipient_entry = tk.Entry(root, width=40)
    recipient_entry.pack(pady=5)
    recipient_entry.insert(0, "Recipient Name")

    message_entry_pv = tk.Entry(root, width=40)
    message_entry_pv.pack(pady=5)
    message_entry_pv.insert(0, "Message")

    shift_entry = tk.Entry(root, width=40)
    shift_entry.pack(pady=5)
    shift_entry.insert(0, "Shift Amount")

    private_button = tk.Button(root, text="Send Private Message", command=lambda: send_private_message(
        client, recipient_entry, message_entry_pv, shift_entry, name, chat_box))
    private_button.pack(pady=5)

    tk.Label(root, text="Block User").pack(pady=5)
    block_entry = tk.Entry(root, width=40)
    block_entry.pack(pady=5)

    block_button = tk.Button(root, text="Block", command=lambda: block_user(client, block_entry))
    block_button.pack(pady=5)

    tk.Label(root, text="Login").pack(pady=5)
    login_frame = tk.Frame(root)
    login_frame.pack(pady=5)

    tk.Label(login_frame, text="Username").grid(row=0, column=0, padx=5)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, padx=5)

    tk.Label(login_frame, text="Password").grid(row=1, column=0, padx=5)
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5)

    login_button = tk.Button(root, text="Login", command=lambda: login(client, username_entry, password_entry))
    login_button.pack(pady=5)

    threading.Thread(target=receive_messages, args=(client, chat_box), daemon=True).start()

    root.mainloop()


def start_client():
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5050

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((IP, PORT))
    except ConnectionError:
        messagebox.showerror("Error", "Unable to connect to the server.")
        return

    name = input("Enter your name: ")
    client.send(name.encode('utf-8'))

    setup_gui(client, name)


if __name__ == "__main__":
    start_client()
