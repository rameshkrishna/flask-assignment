#python smallest size image alpine 
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10-2020-12-19

COPY ./requirements.txt /app/requirements.txt

#gcc is req resolve dependency issues and install 
RUN apk add build-base
RUN apk add --no-cache --virtual .build-deps gcc musl-dev

#install pip req
RUN pip install --no-cache-dir -r /app/requirements.txt

#del build files
RUN apk del .build-deps

#RUN pip install -r /app/requirements.txt
COPY ./ /app

WORKDIR /app

CMD ["uvicorn", "main:app", "--host","0.0.0.0","--port","7070"]
