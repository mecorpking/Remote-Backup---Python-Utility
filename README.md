# CKBackup - Protect Your Data Service

CKBackup is a Windows service that automates the backup of files or folders to FTP/SFTP destinations. It runs as a Windows service and can be set up for regular backups, with the ability to remove old backups automatically.

## Features
- Automated backups of specified folders to FTP/SFTP servers.
- Configurable backup schedule (default: every 24 hours).
- Automatic deletion of old backups based on a specified retention period.
- Detailed logging for monitoring and debugging.

## Prerequisites
- Python 3.x installed on your system.
- The following Python modules:
  - `pywin32` for Windows service management (`pip install pywin32`)
  - `paramiko` for SFTP support (`pip install paramiko`)

## Installation and Service Commands

### 1. Install the Service
Run the following command to install the service and set it to start automatically at boot:
```bash
python main.py --startup auto install
```
### 2. Start the Service
```
sc start CKBackupService
```
### 3. Stop the Service
```
sc stop CKBackupService
```
### To Unistall the Service
```
python main.py remove
```
## Setup Config File - backup_config.json
The service uses a backup_config.json file for configuration. Ensure this file is in the same directory as main.py with the following structure:
```
{
  "folder_path": "path_to_backup_folder",
  "server": "ftp_or_sftp_server_address",
  "port": 21,  // Use 22 for SFTP
  "username": "your_username",
  "password": "your_password",
  "protocol": "ftp",  // or "sftp"
  "backup_period": 30  // Number of days to retain old backups
}
```
## Running in Debug Mode
```
python main.py debug
```
