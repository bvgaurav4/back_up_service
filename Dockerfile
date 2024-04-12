FROM python:3.9-slim

WORKDIR /app

ADD . /app

# COPY creds2.json /app/creds2.json

ENV PYTHONUNBUFFERED=1

RUN pip install  -r requirements.txt

EXPOSE 80

CMD ["python", "lol4.py"]