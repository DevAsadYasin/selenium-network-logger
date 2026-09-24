FROM python:3.11-slim

# Install Chromium browser and ChromeDriver dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for headless Chrome execution in Docker
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "examples/basic_usage.py"]
