FROM python:3.6

ADD . /processor_box

WORKDIR /processor_box

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./start.py" ]
