FROM python:3.11.7-slim-bullseye


# show logs in python
ENV PYTHONUNBUFFERED = 1

#update kernal + install
RUN apt-get update && apt-get -y install gcc libpq-dev

#folder for my project
WORKDIR /app

#copy requirments
COPY requirements.txt /app/requirements.txt

#install req
RUN pip install -r /app/requirements.txt

#copy all project files
COPY . /app/