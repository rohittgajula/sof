# Use the official Python image
FROM python:3.10-slim

# Prevents .pyc files from being written (optional)
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies (if required)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Copy the app's source code into the container
COPY . /app/

# Expose the port that the app runs on
EXPOSE 8000

# Run database migrations and start the Django server
CMD [ "sh", "-c", "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000" ]
