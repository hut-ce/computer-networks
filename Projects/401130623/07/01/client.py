from ftplib import FTP

def upload():
    ftp = FTP()
    ftp.connect("127.0.0.1", 21)  
    ftp.login("auth", "yas83")  
    filename = "file.txt"
    with open(filename, "rb") as file:
        ftp.storbinary(f"Stor {filename}", file)

    print(f"The {filename} uploaded.")
    ftp.quit()
    
def download():
    ftp = FTP()
    ftp.connect("127.0.0.1", 21)  
    ftp.login("auth", "yas83")  
    filename = "file.txt"
    with open(f"downloaded_{filename}", "wb") as file:
        ftp.retrbinary(f"Retr {filename}", file.write)
    print(f"The {filename} downloaded.")
    ftp.quit()

if __name__ == "__main__":
    with open("file.txt", "w") as file :
        file.write("TEST...")

    upload()
    download()