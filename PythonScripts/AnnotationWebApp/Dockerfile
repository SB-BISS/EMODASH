FROM python:2.7

WORKDIR /app

ADD . /app

RUN apt-get update && \
      apt-get -y install apt-utils sudo

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]
