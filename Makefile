.PHONY: clean tg default

default: tg pyvenv

tg:
	cd externals/tg; ./configure; make -j

pyvenv:
	pyvenv venv
	venv/bin/pip install --upgrade -r requirements.txt

clean:
	rm -r venv
