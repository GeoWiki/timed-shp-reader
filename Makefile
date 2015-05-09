
venv:
	virtualenv --python=/usr/bin/python3 venv
	source venv/bin/activate && pip install pyshp