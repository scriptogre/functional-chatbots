# Use an official Python runtime as the base image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file to the working directory
COPY requirements.txt /code/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the working directory
COPY . /code/

# Expose the application on port 8000
EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000