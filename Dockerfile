FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y

WORKDIR /app

COPY . /app


RUN pip3 install -r requirements.txt
EXPOSE 8000

CMD ["python3", "run.py"]