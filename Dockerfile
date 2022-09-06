FROM python:3.10-slim

MAINTAINER 1ris "ediath462@gmail.com"

WORKDIR ./dounaiSign

ADD . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./src/main.py"]