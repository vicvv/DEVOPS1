# https://docs.docker.com/get-started/part2/#apppy

# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN pip install -r requirements.txt

# Run ws.py when the container launches
#CMD ["nameko", "run","ws"]

CMD nameko run --config ./ip.yaml ws 
