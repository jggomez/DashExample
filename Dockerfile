FROM python:3.9-slim-buster

# set working directory in container
WORKDIR /usr/src/app

# Copy and install packages
COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# Copy app folder to app folder in container
COPY /src /usr/src/app/

# Changing to non-root user
RUN useradd -m appUser
USER appUser

# Run locally
CMD gunicorn --bind 0.0.0.0:8080 dashtest:server