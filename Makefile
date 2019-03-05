
.PHONY: default
default: install

.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run python ilswlol/main.py
