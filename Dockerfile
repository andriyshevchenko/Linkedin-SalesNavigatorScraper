# Use an official Python runtime as a parent image
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    privoxy \
    proxychains \
    libx11-dev \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libatspi2.0-0 \
    libgtk-3-0 \
    xdg-utils \
    libgbm-dev \
    libpangocairo-1.0-0 \
    libpq-dev \
    build-essential \
    python3-dev \
    ca-certificates \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Set environment variables for SOCKS5 proxy
ENV ENV_SOCKS5_PROXY_IP=""
ENV ENV_SOCKS5_PROXY_PORT=""
ENV ENV_SOCKS5_PROXY_USERNAME=""
ENV ENV_SOCKS5_PROXY_PASSWORD=""
ENV ENV_HTTP_PROXY_PORT=8118

ENV ENV_DOCKER=1

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its dependencies
RUN playwright install chromium --with-deps

# Copy the rest of your application code into the container
COPY . .

# Configure Proxychains to use SOCKS5 with authentication
RUN echo "strict_chain\n\
proxy_dns\n\
[ProxyList]\n\
socks5 $ENV_SOCKS5_PROXY_IP $ENV_SOCKS5_PROXY_PORT $ENV_SOCKS5_PROXY_USERNAME $ENV_SOCKS5_PROXY_PASSWORD" > /etc/proxychains.conf

# Configure Privoxy to route only specific websites through the SOCKS5 proxy
RUN echo "listen-address 0.0.0.0:$ENV_HTTP_PROXY_PORT\n\
permit-access 0.0.0.0/0\n\
logfile /var/log/privoxy/logfile\n\
filter 0  # Disable filtering\n\
# Forward requests to linkedin.com and its subdomains through the SOCKS5 proxy\n\
forward-socks5t /api.ipify.org/ 127.0.0.1:9050 .\n\
forward-socks5t /linkedin.com/ 127.0.0.1:9050 .\n\
forward-socks5t /www.linkedin.com/ 127.0.0.1:9050 .\n" > /etc/privoxy/config

# Expose Privoxy port
EXPOSE 8118

# Start Privoxy in the background and then run the Python app
CMD privoxy /etc/privoxy/config & \
    proxychains python main.py
