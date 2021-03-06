FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get install -y \
            python-psycopg2 \
            ffmpeg \
            gettext \
            postgresql \
            libavcodec-extra \
        && apt-get clean

RUN mkdir /code
WORKDIR /code
ADD dev_requirements.txt /code/
RUN pip install -r dev_requirements.txt
ADD . /code/