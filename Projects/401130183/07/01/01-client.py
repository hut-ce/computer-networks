from ftplib import FTP

ftp = FTP()
ftp.connect("127.0.0.1", 2121)
ftp.login("user", "12345")

ftp.retrlines("LIST")

filename_to_upload = "test_upload.txt"
with open(filename_to_upload, "rb") as file:
    ftp.storbinary(f"STOR {filename_to_upload}", file)

filename_to_download = "test_download.txt"
with open(filename_to_download, "wb") as file:
    ftp.retrbinary(f"RETR {filename_to_download}", file.write)

ftp.quit()