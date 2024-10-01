# First stage: build
FROM python:3.11-slim AS builder

# Install necessary build tools and libraries
RUN apt-get update && apt-get install -y \
    libgbm-dev \
    libpq-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its dependencies
RUN pip install playwright \
    && playwright install chromium --with-deps

# Second stage: runtime
FROM python:3.11-slim

# Install necessary runtime packages, including Privoxy
RUN apt-get update && apt-get install -y \
    curl \
    lsof \
    privoxy \
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
    libasound2 \
    xdg-utils \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the Playwright browsers installed in the builder stage
COPY --from=builder /root/.cache/ms-playwright /root/.cache/ms-playwright

# Copy application code into the container
COPY . .

ENV ENV_DOCKER=1
ENV ENV_HTTP_PROXY_IP='127.0.0.1'

# Inline Privoxy configuration with SOCKS5 authentication
RUN echo "forward-socks5 / {ENV_SOCKS5_PROXY_USERNAME}:{ENV_SOCKS5_PROXY_PASSWORD}@{ENV_SOCKS5_PROXY_IP}:{ENV_SOCKS5_PROXY_PORT} ." >> /etc/privoxy/config && \
    echo "listen-address  $ENV_HTTP_PROXY_IP:{ENV_HTTP_PROXY_PORT}" >> /etc/privoxy/config

# Make the script executable
RUN chmod +x /app/start-services.sh

# Use the shell script to start services and run the Python application
CMD ["/app/start-services.sh"]
