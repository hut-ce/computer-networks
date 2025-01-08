from ftplib import FTP

def upload_file():
    ftp = FTP()
    ftp.connect("127.0.0.1", 2121)  
    ftp.login("user", "password")  

   
    filename = "example.txt"
    with open(filename, "rb") as file:
        ftp.storbinary(f"STOR {filename}", file)

    print(f"{filename} uploaded successfully.")
    ftp.quit()

def download_file():
    ftp = FTP()
    ftp.connect("127.0.0.1", 2121)  
    ftp.login("user", "password")  

   
    filename = "example.txt"
    with open(f"downloaded_{filename}", "wb") as file:
        ftp.retrbinary(f"RETR {filename}", file.write)

    print(f"{filename} downloaded successfully.")
    ftp.quit()

if __name__ == "__main__":
    
    server_thread = Thread(target=start_ftp_server, daemon=True)
    server_thread.start()

    
    with open("example.txt", "w") as f:
        f.write("This is a test file for FTP.")

    
    upload_file()
    download_file()