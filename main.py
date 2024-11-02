import os
import sys
import time
import win32service
import win32serviceutil
import win32event
import json
import shutil
import paramiko
from ftplib import FTP
import logging

# Configure logging to file
LOG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'backup_service.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,  # Change to DEBUG for detailed output
    format='%(asctime)s - %(levelname)s - %(message)s'
)

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'backup_config.json')  # Ensure the correct path

class BackupService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'CKBackupService'
    _svc_display_name_ = 'CKBackup - Protect Your Data'
    _svc_description_ = 'A service to back up files or folders to FTP/SFTP destinations.'

    def __init__(self, args):
        if 'debug' in args:
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            self.running = True
            logging.info("Service initialized in debug mode.")
        else:
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            self.running = True
            logging.info("Service initialized.")

    def SvcStop(self):
        self.running = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        logging.info("Service is stopping...")

    def SvcDoRun(self):
        logging.info("Service is starting...")
        try:
            self.main()
        except Exception as e:
            logging.error(f"Service encountered an error: {str(e)}")
        logging.info("Service has exited SvcDoRun.")

    def load_config(self):
        logging.info("Loading configuration...")
        if not os.path.exists(CONFIG_FILE):
            logging.error("Configuration file not found. Exiting.")
            return None

        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                logging.info("Configuration loaded successfully.")
                return config
        except Exception as e:
            logging.error(f"Failed to load configuration: {str(e)}")
            return None

    def create_ftp_client(self, config):
        try:
            ftp = FTP()
            ftp.connect(config['server'], config.get('port', 21))
            ftp.login(config['username'], config['password'])
            logging.info("FTP client connected successfully.")
            return ftp
        except Exception as e:
            logging.error(f"Failed to create FTP client: {str(e)}")
            raise

    def create_sftp_client(self, config):
        try:
            transport = paramiko.Transport((config['server'], config.get('port', 22)))
            transport.connect(username=config['username'], password=config['password'])
            sftp = paramiko.SFTPClient.from_transport(transport)
            logging.info("SFTP client connected successfully.")
            return sftp
        except Exception as e:
            logging.error(f"Failed to create SFTP client: {str(e)}")
            raise

    def main(self):
        logging.info("Starting main function...")
        config = self.load_config()
        if not config:
            logging.error("Configuration is missing. Exiting service.")
            return

        logging.info("Configuration loaded, starting backup loop...")

        if not config.get('folder_path') or not config.get('server'):
            logging.error("Configuration is incomplete. Exiting service.")
            return

        while self.running:
            try:
                logging.info("Starting backup process...")
                date_str = time.strftime("%Y-%m-%d")
                folder_name = os.path.basename(config['folder_path'].rstrip('/\\'))
                zip_filename = f"{folder_name}_{date_str}.zip"
                zip_path = os.path.join("C:\\tmp", zip_filename)  # Use absolute path for Windows

                if not os.path.exists("C:\\tmp"):
                    os.makedirs("C:\\tmp")
                    logging.info("Created C:\\tmp directory for temporary zip storage.")

                # Create a zip archive of the folder
                shutil.make_archive(zip_path.replace('.zip', ''), 'zip', config['folder_path'])
                logging.info(f"Created zip file: {zip_path}")

                # Upload the zip file
                if config['protocol'] == 'ftp':
                    ftp_client = self.create_ftp_client(config)
                    with open(zip_path, 'rb') as f:
                        ftp_client.storbinary(f'STOR {zip_filename}', f)
                    ftp_client.quit()
                    logging.info(f"Uploaded {zip_filename} to FTP server.")

                elif config['protocol'] == 'sftp':
                    sftp_client = self.create_sftp_client(config)
                    sftp_client.put(zip_path, f"/{zip_filename}")
                    sftp_client.close()
                    logging.info(f"Uploaded {zip_filename} to SFTP server.")

                # Remove the local zip file after upload
                os.remove(zip_path)
                logging.info(f"Removed local zip file: {zip_path}")

                # Remove old backups
                self.remove_old_backups(config)

            except Exception as e:
                logging.error(f"Backup failed: {str(e)}")

            # Wait 24 hours before the next backup cycle
            logging.info("Waiting for the next backup cycle...")
            time.sleep(24 * 3600)

    def remove_old_backups(self, config):
        logging.info("Starting to remove old backups...")
        cutoff_date = (time.time() - (config['backup_period'] * 24 * 3600))

        try:
            if config['protocol'] == 'ftp':
                ftp_client = self.create_ftp_client(config)
                for filename in ftp_client.nlst():
                    try:
                        date_str = filename.split('_')[-1].replace('.zip', '')
                        file_date = time.mktime(time.strptime(date_str, "%Y-%m-%d"))
                        if file_date < cutoff_date:
                            ftp_client.delete(filename)
                            logging.info(f"Deleted old backup {filename} from FTP server.")
                    except Exception as e:
                        logging.warning(f"Failed to delete {filename}: {str(e)}")
                ftp_client.quit()

            elif config['protocol'] == 'sftp':
                sftp_client = self.create_sftp_client(config)
                for filename in sftp_client.listdir():
                    try:
                        date_str = filename.split('_')[-1].replace('.zip', '')
                        file_date = time.mktime(time.strptime(date_str, "%Y-%m-%d"))
                        if file_date < cutoff_date:
                            sftp_client.remove(filename)
                            logging.info(f"Deleted old backup {filename} from SFTP server.")
                    except Exception as e:
                        logging.warning(f"Failed to delete {filename}: {str(e)}")
                sftp_client.close()

        except Exception as e:
            logging.error(f"Failed to remove old backups: {str(e)}")

if __name__ == '__main__':
    logging.info("Service script started directly.")
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        logging.info("Running in debug mode.")
        service = BackupService(['debug'])  # Pass 'debug' as a simulated argument
        service.SvcDoRun()  # Run service logic manually for debugging
    else:
        win32serviceutil.HandleCommandLine(BackupService)