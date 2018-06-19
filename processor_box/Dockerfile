FROM python:3.6

WORKDIR /processor_box

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./redis_subscriber.py" ]

