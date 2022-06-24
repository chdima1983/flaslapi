FROM python:3.7.4-alpine3.10
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
#COPY /flask-api /flask-api
ENTRYPOINT ["python"]
CMD ["api.py"]