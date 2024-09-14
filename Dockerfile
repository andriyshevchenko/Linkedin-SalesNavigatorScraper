# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install necessary packages and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb 

# Set the working directory
WORKDIR /app

ENV ENV_DOCKER=1

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose any necessary ports (optional, depending on your application)
# EXPOSE 8080

# Command to run your application
CMD ["python", "main.py"]
