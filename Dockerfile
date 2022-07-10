FROM python:latest
RUN apt-get update -y && apt-get install -y python3-pip && apt-get install -y python && apt-get install -y python3
RUN apt-get install -y g++ && apt-get install -y python3-dev && apt-get install -y libffi-dev
#    apk add --no-cache --update python3 && \
RUN /bin/bash -c "pip3 install --upgrade pip setuptools"
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
#COPY /flask-api /flask-api
ENTRYPOINT ["python"]
CMD ["api.py"]

#FROM python:latest

#RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
#    apk add --no-cache --update python3 && \
#    pip3 install --upgrade pip setuptools
#COPY requirements.txt requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
#COPY /flask-api /flask-api
ENTRYPOINT ["python"]
CMD ["api.py"]