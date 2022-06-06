
install:
	#pip install --upgrade pip &&\
	#	pip install -r requirements.txt
	pip install pandas
	pip install matplotlib
	pip install notebook
	pip install pillow
	pip install pixelate
	pip install imgkit
	pip install wkhtmltopdf

lint:
	pylint --disable=R,C main.py

test:
	#python -m pytest -vv --cov=base test_base.py
	pytest -v
