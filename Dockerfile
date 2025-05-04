FROM ubuntu:22.04

COPY . /site

WORKDIR /site

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y python3 python3-pip
RUN	pip install -r requirements.txt

CMD ["python3", "src/app.py"]

