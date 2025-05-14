FROM ubuntu:22.04

COPY . /site

WORKDIR /site

RUN apt update -y
# RUN apt upgrade -y
RUN apt install -y python3 python3-pip
RUN pip install -r requirements.txt

RUN python3 src/backend/init_db.py
RUN chmod 755 start_app.sh
RUN ls -la

CMD ["./start_app.sh"]

