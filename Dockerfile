FROM ubuntu:20.04 
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /nlp-suite

RUN apt-get update && apt-get install -y python3.9 python3.9-dev python3-pip python3-tk 

RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install --upgrade setuptools

COPY . .

RUN python3.9 -m pip install -r requirements.txt

WORKDIR /nlp-suite/src
EXPOSE 3000
CMD ["python3.9", "main.py"]
