#!/bin/bash

# Function to check if Privoxy is running
check_privoxy() {
    if curl -s --connect-timeout 2 http://$ENV_HTTP_PROXY_IP:$ENV_HTTP_PROXY_PORT/ > /dev/null; then
        return 0  # Privoxy is running
    else
        return 1  # Privoxy is not running
    fi
}

# Find a free port
find_free_port() {
    while true; do
        # Generate a random port number between 1024 and 65535
        PORT=$(shuf -i 1024-65535 -n 1)
        
        # Check if the port is free using lsof
        if ! lsof -iTCP:$PORT -sTCP:LISTEN > /dev/null; then
            echo $PORT
            break
        fi
    done
}

export ENV_HTTP_PROXY_PORT=$(find_free_port)

echo "Replace the placeholder with the actual port"

# Replace the placeholder with the actual port
sed -i -e "s/{ENV_HTTP_PROXY_PORT}/$ENV_HTTP_PROXY_PORT/g" \
       -e "s/{ENV_SOCKS5_PROXY_USERNAME}/$ENV_SOCKS5_PROXY_USERNAME/g" \
       -e "s/{ENV_SOCKS5_PROXY_PASSWORD}/$ENV_SOCKS5_PROXY_PASSWORD/g" \
       -e "s/{ENV_SOCKS5_PROXY_IP}/$ENV_SOCKS5_PROXY_IP/g" \
       -e "s/{ENV_SOCKS5_PROXY_PORT}/$ENV_SOCKS5_PROXY_PORT/g" /etc/privoxy/config

echo "Using port $ENV_HTTP_PROXY_PORT for Privoxy."

# Start Privoxy with the environment variable override
privoxy --no-daemon /etc/privoxy/config &

# Wait for Privoxy to start
until check_privoxy; do
    echo "Waiting for Privoxy to start on port $ENV_HTTP_PROXY_PORT..."
    sleep 5
done

echo "Privoxy started successfully on port $ENV_HTTP_PROXY_PORT."

# Now run the Python application
python main.py
