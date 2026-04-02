init:
	python -m venv venv

install:
	. venv/bin/activate && pip install -e .[test]

test:
	. venv/bin/activate && pytest -vs