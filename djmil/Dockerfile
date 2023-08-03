FROM python:latest

WORKDIR /DjmilApps


COPY requirements.txt ./

RUN pip install --upgrade  pip
RUN pip install -r requirements.txt

COPY djmil ./
