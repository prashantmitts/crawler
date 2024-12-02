# Use Python 3.9 slim as the base image
FROM python:3.9-slim-buster as base

# Set environment variable to ensure Python output is not buffered
ENV PYTHONUNBUFFERED=1

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    chromium \
    chromium-driver \
    build-essential \
    libpq-dev \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app/

# Create a virtual environment, upgrade pip, and install Python dependencies
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip

# Enable the virtual environment by updating PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file into the container and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Set environment variables for Selenium to locate Chromium and Chromedriver
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Validate installations (optional but helpful for debugging)
RUN echo "Chromium path: $CHROME_BIN" && \
    echo "Chromedriver path: $CHROMEDRIVER_PATH" && \
    $CHROME_BIN --version && \
    $CHROMEDRIVER_PATH --version

# Set the default command to run the application
CMD ["python", "monitoring.py"]
