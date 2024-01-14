# Use an official Python runtime as a parent image
FROM python:3.12.1-slim-bullseye

# Set the working directory in the container
WORKDIR /app/blockwise
ENV HOME /app

ADD requirements.txt /app/blockwise/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
ADD . /app/blockwise

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=blockwise.settings

# run as daemon user
USER daemon
# Run app.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "blockwise.wsgi:application"]
