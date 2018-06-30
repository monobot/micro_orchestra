FROM python:3.6

ADD . /final_box

WORKDIR /final_box

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./start.py" ]
