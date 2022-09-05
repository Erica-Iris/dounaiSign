FROM python:3.7

MAINTAINER 1ris "ediath462@gmail.com"

WORKDIR ./dounaiSign

ADD . .

RUN pip install -r requirements.txt

CMD ["python", "./src/main.py"]