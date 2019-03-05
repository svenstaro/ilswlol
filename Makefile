.PHONY: default
default: install

.PHONY: install
install:
	poetry install --develop .

.PHONY: run
run:
	poetry run python -m sanic ilswlol.app --host=0.0.0.0 --port=8080 --worker=4
