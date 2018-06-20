FROM python:3
MAINTAINER SHARAD BAIDYA

ENV BASE_URL='http://13.230.100.118:5000/'

COPY . /home/docker/

RUN pip install -r /home/docker/requirements.txt
WORKDIR /home/docker

CMD ["python", "app.py"]