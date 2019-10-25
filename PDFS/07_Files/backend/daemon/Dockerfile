# Use python3
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app


# Install psutils
RUN pip install -r requirements.txt

CMD nameko run daemon

