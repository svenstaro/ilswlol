.PHONY: clean tg default
CC = gcc
CFLAGS = -g -Wall

default: tg pyvenv
	echo "rofl"

tg:
	cd externals/tg; ./configure; make -j

pyvenv:
	pyvenv venv
	venv/bin/pip install --upgrade -r requirements.txt

clean:
	echo "lol"
