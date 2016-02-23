.PHONY: clean tg default

default: tg pyvenv

tg:
	cd externals/tg; ./configure; make -j

pyvenv:
	pyvenv venv
	venv/bin/pip install --upgrade -r requirements.txt

run:
	venv/bin/python ilswlol/__init__.py

clean:
	rm -r venv
