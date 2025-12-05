# Use a lightweight Python base image
FROM python:3.9-slim

# Install system dependencies required for image processing libraries
# rembg/u2net depends on these libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
# This will also download the U2NET model on the first build, 
# ensuring it's ready for production
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py .

# Create a hidden folder for u2net to avoid permission issues if the model downloads at runtime
# (Though rembg usually handles this, it's good practice for containers)
RUN mkdir -p /root/.u2net

# Expose the port Railway will use
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]