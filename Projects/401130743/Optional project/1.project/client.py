from ftplib import FTP
from threading import Thread

def send_files():
    myftp = FTP()

    myftp.connect("127.0.0.1", 2121)  
    myftp.login("user", "password")  

   
    file = "example.txt"

    with open(file, "rb") as file:
        myftp.storbinary(f"STOR {file}", file)

    print(f"{file} uploaded successfully.")
    myftp.quit()

def receive_file():
    myftp = FTP()

    myftp.connect("127.0.0.1", 2121)  
    myftp.login("user", "password")  

   
    file = "example.txt"

    with open(f"downloaded_{file}", "wb") as file:
        myftp.retrbinary(f"RETR {file}", file.write)

    print(f"{file} downloaded successfully.")
    myftp.quit()

if __name__ == "__main__":
    
    server_thread = Thread(target=start_ftp_server, daemon=True)
    server_thread.start()

    
    with open("example.txt", "w") as f:
        f.write("This is a test file for FTP.")

    
    send_files()
    receive_file()