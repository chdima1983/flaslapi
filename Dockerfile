 FROM python:3.8-slim-buster

EXPOSE 5000

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /flask-api
#COPY /flask-api /flask-api
ADD /flask-api/ /flask-api/

CMD [ "python", "api.py" ]