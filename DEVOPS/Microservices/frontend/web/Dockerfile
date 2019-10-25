# https://docs.docker.com/get-started/part2/#apppy

# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN pip install -r requirements.txt

#RUN echo "America/Los_Angeles" > /etc/timezone
#RUN dpkg-reconfigure -f noninteractive tzdata

# Run frontend.py when the container launches
#CMD ["nameko", "run","frontend"]

CMD nameko run --config ./ip.yaml frontend
