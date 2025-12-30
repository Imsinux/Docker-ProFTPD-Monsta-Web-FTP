# 🐳 Docker ProFTPD + Monsta Web FTP

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![ProFTPD](https://img.shields.io/badge/Server-ProFTPD-green?style=for-the-badge)
![MonstaFTP](https://img.shields.io/badge/Client-Monsta_FTP-orange?style=for-the-badge)

> **A secure, containerized FTP ecosystem.**
> Seamless web-based file management coupled with a robust backend and automated pythonic user control.

---

## 📖 Overview

This solution deploys a hardened **ProFTPD** server alongside **Monsta FTP** (a PHP web client). It solves the common headache of FTP permissions by utilizing a "Smart Isolation" strategy, allowing users to collaborate in public folders while keeping private data locked down.

### 🌟 Key Features

| Feature | Description |
| :--- | :--- |
| **📦 Containerized** | ProFTPD and Monsta run in isolated containers, keeping your host clean. |
| **🌐 Web Interface** | No FTP client needed—manage files directly via browser. |
| **🐍 Python Automation** | Custom script (`manage_ftp.py`) handles UID generation and user creation. |
| **🔐 Smart Permissions** | Automated `Public` (RW access for all) and `Private` (Owner only) folder structure. |
| **🔄 Hybrid Network** | Pre-configured for Docker internal networking or external passive mode. |

---

## 🏗️ Architecture

```text
      +--------+
      |  User  |
      +---+----+
          |
    +-----+------+
    |            | Browser (HTTP)
    |      +-----v-------+
    |      | Monsta FTP  |
    |      | (Container) |
    |      +-----+-------+
    |            |
    | FTP        | Docker Internal Network
    |            |
    |      +-----v-------+       +-------------+
    +----->|  ProFTPD    +------->  Local Disk |
           | (Container) | Mount |   (/data)   |
           +-------------+       +-------------+
Directory Structure
When you create a user, the system automatically builds this structure:

Plaintext

/home/ftp/
├── username/
│   ├── Public/   [ ✅ Everyone Read/Write ]
│   └── Private/  [ 🔒 User Only (chmod 700) ]
🚀 Quick Start
1. Prerequisites
Docker & Docker Compose

Python 3 (Host machine)

2. Launch Services
Clone the repo and fire up the containers:

Bash

git clone <your-repo-url>
cd <your-repo-folder>
docker-compose up -d
3. 🛡️ Initialize Security (Critical)
ProFTPD requires the password database to have strict permissions, or it will refuse to start.

[!IMPORTANT] Run this command immediately after cloning:

Bash

# Create the DB and lock permissions
touch config/ftpd.passwd
chmod 600 config/ftpd.passwd
⚙️ Network Configuration
Choose the scenario that fits your needs.

🟢 Scenario A: Web-Only (Internal Docker Network)
Best for using Monsta FTP exclusively.

Edit: config/proftpd.conf

Setting: Ensure Masquerade is disabled.

Apache

# MasqueradeAddress 1.2.3.4  <-- Commented out
Login Host: Use ftp_server (The container name).

🟠 Scenario B: External Access (FileZilla / Remote)
Best if you need to connect via desktop FTP clients from outside the network.

Edit: config/proftpd.conf

Setting: Enable Masquerade with your Public IP.

Apache

MasqueradeAddress 123.45.67.89  <-- Your VPS/Server IP
Firewall: Open ports 21 and 60000-60100.

👤 User Management
Forget manual config editing. Use the Python helper in /scripts.

Add a User
Generates a unique UID, adds to the auth DB, and builds directory structure.

Bash

cd scripts
python3 manage_ftp.py add <username> '<password>'
Delete a User
Removes the user from the authentication database immediately.

Bash

cd scripts
python3 manage_ftp.py del <username>
🔧 Troubleshooting
<details> <summary><strong>❌ Upload Failed: Unable to switch to passive mode</strong></summary>

Cause: IP Mismatch. You are using an IP address to connect, but the server is expecting the Docker container name, or MasqueradeAddress is set incorrectly.

Fix:

If using Monsta Web: Set Host to ftp_server.

Ensure MasqueradeAddress is commented out in proftpd.conf for web usage.

docker restart ftp_server

</details>

<details> <summary><strong>🚫 Permission Denied inside Public folder</strong></summary>

Cause: Host file permissions became misaligned (often happens if you move files manually as root).

Fix: Run this "One-Liner" on your host machine to reset strict permissions:

Bash

# Reset all folder visibility, unlock Public, and lock Private
find data -mindepth 1 -maxdepth 1 -type d -exec chmod 755 {} + && \
find data -name "Public" -type d -exec chmod 777 {} + && \
find data -name "Private" -type d -exec chmod 700 {} +
</details>

<p align="center"> <sub>Managed by <a href="#">YourName/Organization</a></sub> </p>
