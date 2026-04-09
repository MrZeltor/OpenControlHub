FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for GUI/PyAutoGUI if needed (Headless warning)
RUN apt-get update && apt-get install -y \
    python3-tk \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
