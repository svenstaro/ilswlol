.PHONY: clean default venv run

default: venv

venv:
	python -m venv venv
	venv/bin/pip install --upgrade -r requirements.txt

run:
	venv/bin/uwsgi --ini uwsgi_local_dev.ini

clean:
	rm -r venv
