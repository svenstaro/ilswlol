FROM python:3.7
MAINTAINER Sven-Hendrik Haase <svenstaro@gmail.com>

ADD . /app
WORKDIR /app
RUN pip3 install poetry && poetry install

EXPOSE 8000

CMD ["poetry", "run", "python", "runner.py"]
