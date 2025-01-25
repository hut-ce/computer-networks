import ftplib
import os

class FTPClient:
    def init(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ftp = ftplib.FTP()

    def connect(self):
        try:
            self.ftp.connect(self.host)
            self.ftp.login(self.username, self.password)
            print("Connected.")
        except ftplib.all_errors as e:
            print(f"error: {e}")

    def upload_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                self.ftp.storbinary(f'STOR {os.path.basename(file_path)}', file)
                print(f"Uploaded {file_path}.")
        except Exception as e:
            print(f"Failed to upload: {e}")

    def download_file(self, filename, destination):
        try:
            with open(destination, 'wb') as file:
                self.ftp.retrbinary(f'RETR {filename}', file.write)
                print(f"Downloaded {filename} from FTP server to {destination}.")
        except Exception as e:
            print(f"Failed to download: {e}")

    def list_files(self):
        try:
            files = self.ftp.nlst()
            print("Files on the server:")
            for file in files:
                print(file)
        except Exception as e:
            print(f"Failed to list files: {e}")

    def disconnect(self):
        self.ftp.quit()
        print("Disconnected.")

if __name__ == "__main__":

    ftp_host = 'ftp.example.com'
    ftp_username = 'user'
    ftp_password = 'pass'

    client = FTPClient(ftp_host, ftp_username, ftp_password)
    client.connect()
    
    client.list_files()

    client.upload_file('path/to/your/file.txt')

    client.download_file('file.txt', 'path/to/save/file.txt')

    client.disconnect()
