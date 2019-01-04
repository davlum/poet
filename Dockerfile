FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get install -y \
            python-psycopg2 \
            ffmpeg \
            gettext \
            postgresql \
        && apt-get clean

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/