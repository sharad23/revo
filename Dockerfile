FROM python:3
MAINTAINER SHARAD BAIDYA

ENV DOMAIN='http://13.230.100.118/'

COPY . /home/docker/

RUN pip install -r /home/docker/requirements.txt
WORKDIR /home/docker

CMD ["python", "app.py"]