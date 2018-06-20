FROM python:3.6

WORKDIR /publisher_box

ADD . /publisher_box

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./redis_subscriber.py" ]
