.PHONY: clean default venv run

default: venv

venv:
	python -m venv venv
	venv/bin/pip install --upgrade -r requirements.txt

run:
	venv/bin/python ilswlol/__init__.py

clean:
	rm -r venv
