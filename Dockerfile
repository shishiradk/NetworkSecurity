# Use official lightweight Python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy all project files into container
COPY . .

# Install system dependencies and AWS CLI
RUN apt-get update -y && apt-get install -y awscli

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port if needed (optional, e.g., for FastAPI or Flask)
# EXPOSE 8080

# Default command to run your app
CMD ["python", "app.py"]
