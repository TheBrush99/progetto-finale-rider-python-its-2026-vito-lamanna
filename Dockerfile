FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for psycopg2 if needed (though psycopg2-binary usually doesn't need them on modern linux, it's safer)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Start the application
CMD ["python", "main.py"]
