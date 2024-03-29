FROM python:3.9

# Set up code directory
WORKDIR /usr/src/app

# Install linux dependencies
RUN apt-get update && apt-get install -y libssl-dev

RUN apt-get update && apt-get install -y \
    npm

# Install app dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

# Copy app
COPY ./ /usr/src/app/

# Create empty dir for future images and metadata files
RUN mkdir -p /usr/src/app/server_app/src


# Set up directory for brownie and compile
WORKDIR /usr/src/app/brownie_app
RUN brownie compile

# Set up directory and start server
WORKDIR /usr/src/app/
CMD ["sh", "-c", "uvicorn server_app.app:app --host 0.0.0.0 --port 8000"]
