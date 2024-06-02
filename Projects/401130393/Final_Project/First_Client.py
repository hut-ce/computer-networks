import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

# Network configuration
ip = "127.0.0.5"
port = 5050

# Create a client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))  # Connect to the server

# Tkinter GUI setup
root = tk.Tk()
root.withdraw()  # Hide the main window initially

# Ask for the user's name using a dialog box
name = simpledialog.askstring("Name", "Please enter your name:", parent=root)

if not name:
    print("No name provided. Exiting...")
    client.close()  # Close the client socket if no name is provided
    root.quit()
else:
    client.send(name.encode('utf-8'))  # Send the user's name to the server

    root.deiconify()  # Show the main window
    root.title("Chat Client")

    # Frame for displaying messages
    message_frame = tk.Frame(root)
    message_frame.pack()

    # Scrollbar for the message box
    scrollbar = tk.Scrollbar(message_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Text box for displaying messages
    message_box = scrolledtext.ScrolledText(message_frame, height=20, width=50, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    message_box.pack(side=tk.LEFT, fill=tk.BOTH)
    message_box.config(state=tk.DISABLED)

    # Entry widget for typing messages
    message_entry = tk.Entry(root, width=50)
    message_entry.pack()
    message_entry.focus()

    def send_message(event=None):
        """
        Function to send a message to the server.
        """
        message = message_entry.get()
        if message:
            formatted_message = f"{name}: {message}"
            client.send(formatted_message.encode('utf-8'))  # Send the message to the server
            message_box.config(state=tk.NORMAL)
            message_box.insert(tk.END, f"You: {message}\n")  # Display the sent message in the message box
            message_box.config(state=tk.DISABLED)
            message_box.yview(tk.END)
            message_entry.delete(0, tk.END)  # Clear the entry widget

    # Bind the Enter key to the send_message function
    message_entry.bind("<Return>", send_message)

    def receive_message():
        """
        Function to receive messages from the server.
        """
        while True:
            try:
                message = client.recv(1024).decode()  # Receive a message from the server
                if not message:
                    break
                #--------------------Our Changes--------------------------------
                if message.startswith("PRIVATE"):
                    _, sender, private_message = message.split(": ", 2)
                    if sender in private_windows:
                        private_windows[sender].display_message(f"{sender}: {private_message}")
                    else:
                        private_windows[sender] = PrivateChatWindow(root, sender)
                        private_windows[sender].display_message(f"{sender}: {private_message}")
                else:
                    message_box.config(state=tk.NORMAL)
                    message_box.insert(tk.END, message + '\n')  # Display the received message in the message box
                    message_box.config(state=tk.DISABLED)
                    message_box.yview(tk.END)
                #----------------------------------------------------------------
            except ConnectionResetError:
                print("Connection with server is lost!")
                break
            except OSError:
                break  # Exit the loop if the socket is closed

    # Run the receive_message function in a separate thread
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.daemon = True  # Allow the thread to close when the main program exits
    receive_thread.start()

    private_windows = {}
    #-----------------Our new function-------------------------------
    def start_private_chat():
        # Function to create a private chat with another user.
        recipient = simpledialog.askstring("Private Chat", "Enter the name of the user you want to chat with:", parent=root)
        if recipient and recipient != name:
            if recipient not in private_windows:
                private_windows[recipient] = PrivateChatWindow(root, recipient) # Calling the function to open a new window
            else:
                private_windows[recipient].deiconify()

    def send_private_message(recipient, message):
        # Function to send a private message to another user.
        if message:
            formatted_message = f"PRIVATE: {recipient}: {message}"
            client.send(formatted_message.encode('utf-8'))  # Send the private message to the server
    #-------------------Our Class-------------------------------------
    class PrivateChatWindow(tk.Toplevel):
        # Class to open a new chat window for each new chat between new people.
        def __init__(self, master, recipient):
            super().__init__(master)
            self.recipient = recipient
            self.title(f"Private Chat with {recipient}")

            self.message_frame = tk.Frame(self)
            self.message_frame.pack()

            self.scrollbar = tk.Scrollbar(self.message_frame)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.message_box = scrolledtext.ScrolledText(self.message_frame, height=20, width=50, wrap=tk.WORD, yscrollcommand=self.scrollbar.set)
            self.message_box.pack(side=tk.LEFT, fill=tk.BOTH)
            self.message_box.config(state=tk.DISABLED)

            self.message_entry = tk.Entry(self, width=50)
            self.message_entry.pack()
            self.message_entry.focus()

            self.message_entry.bind("<Return>", self.send_private_message)

        def send_private_message(self, event=None):
            """
            Function to send a private message.
            """
            message = self.message_entry.get()
            if message:
                send_private_message(self.recipient, message)
                self.display_message(f"You: {message}")
                self.message_entry.delete(0, tk.END)

        def display_message(self, message):
            """
            Function to display a message in the private chat window.
            """
            self.message_box.config(state=tk.NORMAL)
            self.message_box.insert(tk.END, message + '\n')
            self.message_box.config(state=tk.DISABLED)
            self.message_box.yview(tk.END)
    #---------------------------------------------------------------------------------
    # -------------------------------Our Buttons --------------------------------------
    private_chat_button = tk.Button(root, text="Start Private Chat", command=start_private_chat)
    private_chat_button.pack()
    # --------------------------------------------------------------------------------
    def on_closing(event=None):
        """
        Function to handle the window close event.
        """
        client.close()  # Close the client socket
        root.quit()  # Stop the Tkinter main loop
        root.destroy()  # Destroy the Tkinter window

    # Bind the window close event to the on_closing function
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the Tkinter main loop
    root.mainloop()
