FROM python:3.9.2

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y wkhtmltopdf xvfb

WORKDIR /app

ADD ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ .

EXPOSE 8080

ENV NO_PROXY = "s3.amazonaws.com"

CMD uvicorn main:app --reload