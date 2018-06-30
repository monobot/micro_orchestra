FROM python:3.6

ADD . /publisher_box

WORKDIR /publisher_box

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./start.py" ]
