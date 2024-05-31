install:
		pip install --upgrade pip &&\
			pip install -r requirements.txt
test:
		python -m pytest -v -s

get_list:
		python get_list_docs.py
