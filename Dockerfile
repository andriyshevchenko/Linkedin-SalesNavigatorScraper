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
ENV ENV_FUNCTION_NAME=disconnect-leads
ENV ENV_MAX_ALLOWED_CONNECTION_REQUESTS=150
ENV ENV_SQL_CONNECTION_LEADS_DB_HOST=159.89.13.130
ENV ENV_SQL_CONNECTION_LEADS_DB_PORT=5432
ENV ENV_SQL_CONNECTION_LEADS_DB_NAME=ukraine_it_ceo
ENV ENV_SQL_CONNECTION_LEADS_DB_USER=Administrator
ENV ENV_SQL_CONNECTION_LEADS_DB_PASSWORD=lUwm8vS21jLW
ENV ENV_TELEGRAM_BOT_TOKEN=7209921522:AAHRhEH11Clg_qBPY9SSwfEJDoPvJ5yso70
ENV ENV_TELEGRAM_CHAT_ID=-1002300475780

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
