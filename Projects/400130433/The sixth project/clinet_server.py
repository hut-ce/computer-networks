import socket
import threading
import tkinter as tk
from tkinter import messagebox


def caesar_cipher(message, key):
    result = ""
    for char in message:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result


bad_words = ['fuck', 'airhead', 'bastard']


def filter_bad_words(message):
    for word in bad_words:
        if word in message.lower():
            message = message.replace(word, '*' * len(word))  
    return message


def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            decrypted_message = caesar_cipher(message, -3)  
            text_area.insert(tk.END, decrypted_message + "\n")
            text_area.yview(tk.END)
        except:
            break


def send_message(client_socket, message_entry):
    message = message_entry.get()
    filtered_message = filter_bad_words(message)  
    encrypted_message = caesar_cipher(filtered_message, 3)  
    client_socket.send(encrypted_message.encode())
    message_entry.delete(0, tk.END)


def start_client():
    
    window = tk.Tk()
    window.title("Chat Room")

    
    text_area = tk.Text(window, height=20, width=50)
    text_area.pack()

    message_entry = tk.Entry(window, width=50)
    message_entry.pack()

    send_button = tk.Button(window, text="Send", width=10, command=lambda: send_message(client_socket, message_entry))
    send_button.pack()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    
    name = input("Enter your name: ")
    client_socket.send(name.encode())

    
    threading.Thread(target=receive_messages, args=(client_socket, text_area), daemon=True).start()

    window.mainloop()

if __name__ == "__main__":
    start_client()
