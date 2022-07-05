FROM tiangolo/uwsgi-nginx:python3.10
RUN apt-get update
RUN apt update
RUN apt -y install bash
RUN apt -y install nano
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

