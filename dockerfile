# Use Debian instead of Alpine for better network stability
FROM debian:bookworm-slim

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install ProFTPD
RUN apt-get update && \
    apt-get install -y proftpd-basic && \
    rm -rf /var/lib/apt/lists/*

# Create the user directories and lock files
RUN mkdir -p /run/proftpd && \
    mkdir -p /home/ftp

# Create a system user with UID 1000 to match your Python script
# This ensures file permissions work correctly between Host and Container
RUN useradd -u 1000 -d /home/ftp -s /bin/false ftpuser

# Expose the FTP ports
EXPOSE 21 60000-60100

# Start ProFTPD
CMD ["proftpd", "--nodaemon", "-c", "/etc/proftpd/proftpd.conf"]
