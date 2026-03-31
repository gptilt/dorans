init:
	python -m venv venv

install:
	. venv/bin/activate && pip install -e .[test]