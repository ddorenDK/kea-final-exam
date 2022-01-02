FROM ubuntu:18.04
WORKDIR /usr/src/app
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
 