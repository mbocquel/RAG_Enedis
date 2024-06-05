install:
	pip install --upgrade pip &&\
			pip install -r requirements.txt

lint:
	pylint --disable=R,C,W1203,W0621 *.py */*.py

test:
	python -m pytest -v -s

format:
	black *.py */*.py

all: install lint test format

get_list:
	python get_list_docs.py