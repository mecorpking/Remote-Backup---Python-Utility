from ftplib import FTP

class FTPClient:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password

    def upload_file(self, local_path, remote_path):
        with FTP(self.server) as ftp:
            ftp.login(user=self.username, passwd=self.password)
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_path}', file)

    def list_files(self, remote_path):
        with FTP(self.server) as ftp:
            ftp.login(user=self.username, passwd=self.password)
            ftp.cwd(remote_path)
            return ftp.nlst()

    def delete_file(self, remote_path):
        with FTP(self.server) as ftp:
            ftp.login(user=self.username, passwd=self.password)
            ftp.delete(remote_path)