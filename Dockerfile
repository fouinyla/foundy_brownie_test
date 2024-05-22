FROM python:3.10.5

# Set up code directory
WORKDIR /usr/src/app

# Install linux dependencies
RUN apt-get update && apt-get install --fix-missing -y libssl-dev npm

RUN npm install -g solc

# Install app dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

# Copy app
COPY ./ /usr/src/app/

# Create empty dir for future images and metadata files
RUN mkdir -p /usr/src/app/server_app/src


# Set up directory for brownie and compile
RUN brownie compile
