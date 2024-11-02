import paramiko

class SFTPClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def upload_file(self, local_path, remote_path):
        transport = paramiko.Transport((self.host, 22))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_path, remote_path)
        sftp.close()
        transport.close()

    def list_files(self, remote_path):
        transport = paramiko.Transport((self.host, 22))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        files = sftp.listdir(remote_path)
        sftp.close()
        transport.close()
        return files

    def delete_file(self, remote_path):
        transport = paramiko.Transport((self.host, 22))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.remove(remote_path)
        sftp.close()
        transport.close()