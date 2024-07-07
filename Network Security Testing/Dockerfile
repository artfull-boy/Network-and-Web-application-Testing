# Use an official Kali Linux base image
FROM kalilinux/kali-rolling

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip sudo && \
    apt-get clean

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . /app

# Copy the .env file and export environment variables
COPY .env /app/.env
RUN echo "source /app/.env" >> ~/.bashrc

# Run the application
CMD ["python3", "Network_Testing.py"]
