FROM ubuntu:20.04 
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /nlpsuite

RUN apt-get update && apt-get install -y python3.8 python3.8-dev python3-pip python3-tk 

RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install --upgrade setuptools

COPY src src
COPY lib lib

RUN python3.8 -m pip install -r ./src/requirements.txt

CMD ["python3.8", "./src/NLP_menu_main.py"]
