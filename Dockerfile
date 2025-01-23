# Use a Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy files into the container
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["streamlit", "run", "script2.py"]
