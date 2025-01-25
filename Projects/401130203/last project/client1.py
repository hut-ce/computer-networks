from ftplib import FTP
def connect_to_server():
    f = FTP()
    f.connect("127.0.0.1", 2121)
    f.login("u1", "pass1")
    print("connecting")
    return f
def upload_file(ftp, file_name):
    print("uploading")
    with open(file_name, "rb") as f:
        ftp.storbinary(f"STOR {file_name}", f)
    print("uploaded")
def download_file(ftp, file_name):
    print("downloading")
    with open(file_name, "wb") as f:
        ftp.retrbinary(f"RETR " + file_name, f.write)
    print("downloaded")
def list_files(ftp):
    ftp.retrlines("LIST")
def do_stuff():
    ftp = connect_to_server()
    list_files(ftp)
    upload_file(ftp, "example.txt")
    download_file(ftp, "example.txt")
    print("finish")
    ftp.quit()

do_stuff()
