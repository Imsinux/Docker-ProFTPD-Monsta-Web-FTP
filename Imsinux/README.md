# 📂 Docker ProFTPD + Monsta Web FTP

A secure, Dockerized FTP server solution featuring a web-based file manager (Monsta FTP), a robust ProFTPD backend, and a custom Python script for automated user management.

## 🚀 How It Works
1.  **The Server:** ProFTPD runs in a container, isolated from your host system but mapping data to your local folder.
2.  **The Web Client:** Monsta FTP runs in a separate PHP/Apache container and communicates with the server via Docker's internal network.
3.  **Smart Isolation:**
    * **Root Jail:** Users are jailed to `/home/ftp` but can see other users' folders to facilitate collaboration.
    * **Permissions:**
        * **Public:** Open to everyone (Read/Write).
        * **Private:** Locked to the specific user owner (chmod 700).
4.  **Network Strategy:** The system is pre-configured for internal Docker networking (`AllowForeignAddress on`) to prevent passive mode errors.

---

## 🛠️ Installation Tutorial

### 1. Prerequisites
* Docker & Docker Compose installed on your Linux server.
* Python 3 installed (for the management script).

### 2. Setup
Clone this repository (or download the files) and navigate to the folder:

```bash
# Start the services
docker-compose up -d

3. Initialize Security (Critical Step)
You must create the password database manually on the first run to ensure ProFTPD accepts the file permissions.
# Create the empty file
touch config/ftpd.passwd
# Secure it (ProFTPD will refuse to start if this is World-Readable)
chmod 600 config/ftpd.passwd

⚙️ Configuration Guide (Changing IPs) :

This setup is designed for Monsta FTP to talk to the server locally.
Logging In: When using Monsta FTP, set the Host to ftp_server.

💾2. External Access (FileZilla / Remote)
If you need to connect from a remote PC using an FTP Client (like FileZilla), you must set your Public IP.

File to Edit: config/proftpd.conf

Action: Uncomment the line and set your server's Public IP.
MasqueradeAddress 123.45.67.89  <-- Replace with your Public Server IP


👤 User Management : 
We use a helper script located in scripts/manage_ftp.py to handle UID generation and folder creation automatically.

✅Add a User
This creates the user, generates a unique UID, and builds the Public/Private folders.

cd scripts
python3 manage_ftp.py add username 'your_password'

❌Delete a User
Removes the user from the authentication database.
cd scripts
python3 manage_ftp.py del username
