FROM python:3.9

RUN apt-get update
RUN apt-get install -y iputils-ping

WORKDIR /
COPY mtu.py /mtu.py

ENTRYPOINT ["python", "mtu.py"]
