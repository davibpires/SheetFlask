FROM python:3.6

WORKDIR /sheetflask
COPY requirements.txt /sheetflask

RUN pip install -r /sheetflask/requirements.txt

EXPOSE 5000
