FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p chroma_db uploads

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "server.py"]
