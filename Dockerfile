# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Install the postgresql-dev package
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Set the environment variable FLASK_APP
ENV FLASK_APP app.py

# Expose port 5000
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]



