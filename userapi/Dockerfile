# Stage 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# --- Environment Variables ---
# Set environment variables for the application
# IMPORTANT: Never hardcode sensitive passwords here in a production environment.
# For this project, using environment variables is the correct approach.
ENV MYSQL_HOST=mysql-devops-db
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=my-secret-pw
ENV MYSQL_DB=devops_userdb
ENV FLASK_APP=app.py

# --- Installation ---
# Copy the requirements file i# Dockerfile

# Stage 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# --- FIX: Install build dependencies for mysqlclient and clean up ---
# We use one RUN command to minimize layers and immediately clean up packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libmariadb-dev && \ 
    rm -rf /var/lib/apt/lists/*
# --- End FIX ---


# ... (The ENV variables section remains the same) ...
ENV MYSQL_HOST=mysql-devops-db
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=my-secret-pw 
ENV MYSQL_DB=devops_userdb
ENV FLASK_APP=app.py

# --- Installation ---
# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# --- Application Setup ---
# Copy the rest of the application source code into the container
COPY app.py .

# Expose the port the app runs on (Flask default is 5000)
EXPOSE 5000

# --- Command ---
CMD ["python", "app.py"]nto the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# --- Application Setup ---
# Copy the rest of the application source code into the container
COPY app.py .

# Expose the port the app runs on (Flask default is 5000)
EXPOSE 5000

# --- Command ---
# Run the application when the container launches
CMD ["python", "app.py"]