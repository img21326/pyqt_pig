FROM python:3.7

WORKDIR /usr/src/app

RUN cd /usr/src/app 
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /usr/src/app 
CMD [ "python", "./main.py" ]