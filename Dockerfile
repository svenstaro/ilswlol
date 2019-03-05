FROM python:3.7
MAINTAINER Sven-Hendrik Haase <svenstaro@gmail.com>

ADD . /app
WORKDIR /app
RUN pip3 install poetry && poetry install

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "sanic", "ilswlol.app", "--host=0.0.0.0", "--port=8080", "--workers=4"]

