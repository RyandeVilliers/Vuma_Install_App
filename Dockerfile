FROM python:3.7-alpine
LABEL Ryan de Villiers

ENV PYTHONUNBUFFERED 1

# Copy current directory content to requirements.txt
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# creates empty folder on docker image called /app
RUN mkdir /app

# makes default location
WORKDIR /app

# Copys content of app folder on project to app folder on Docker
COPY ./app /app

# Creates user for running apps only "-D"
RUN adduser -D user

# Switches docker to user we just created - Security Purposes
USER user



