import os
import shutil
import datetime
from zipfile import ZipFile
from .ftp_client import FTPClient
from .sftp_client import SFTPClient

class BackupWorker:
    def __init__(self, local_path, remote_path, backup_period, protocol="ftp", credentials=None):
        self.local_path = local_path
        self.remote_path = remote_path
        self.backup_period = backup_period
        self.protocol = protocol
        self.credentials = credentials

    def create_zip(self):
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        zip_filename = f"{os.path.basename(self.local_path)}_{date_str}.zip"
        zip_path = os.path.join("/tmp", zip_filename)

        with ZipFile(zip_path, 'w') as zipf:
            if os.path.isdir(self.local_path):
                for root, _, files in os.walk(self.local_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, self.local_path))
            else:
                zipf.write(self.local_path, os.path.basename(self.local_path))

        return zip_path

    def upload_zip(self, zip_path):
        if self.protocol == "ftp":
            client = FTPClient(self.credentials["server"], self.credentials["username"], self.credentials["password"])
        elif self.protocol == "sftp":
            client = SFTPClient(self.credentials["server"], self.credentials["username"], self.credentials["password"])
        else:
            raise ValueError("Unsupported protocol")

        client.upload_file(zip_path, os.path.join(self.remote_path, os.path.basename(zip_path)))
        os.remove(zip_path)  # Clean up the local zip file after upload

    def remove_old_backups(self):
        # Logic to connect to the remote server and list/delete files
        # based on the backup period defined by the user
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=self.backup_period)
        if self.protocol == "ftp":
            client = FTPClient(self.credentials["server"], self.credentials["username"], self.credentials["password"])
        elif self.protocol == "sftp":
            client = SFTPClient(self.credentials["server"], self.credentials["username"], self.credentials["password"])
        else:
            raise ValueError("Unsupported protocol")

        backups = client.list_files(self.remote_path)
        for backup in backups:
            if backup.endswith('.zip'):
                date_str = backup.split('_')[-1].replace('.zip', '')
                try:
                    backup_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    if backup_date < cutoff_date:
                        client.delete_file(os.path.join(self.remote_path, backup))
                except ValueError:
                    continue

    def run(self):
        zip_path = self.create_zip()
        self.upload_zip(zip_path)
        self.remove_old_backups()