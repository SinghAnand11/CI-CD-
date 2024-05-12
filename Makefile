install:
	pip install --upgrade pip &&\
        	pip install -r requirements.txt

format:
	black *.py

train:
	python 5083.py

eval:
	echo "## Model Metrics" > results.md
	cat metrics.txt >> results.md
   

	cml comment create results.md
