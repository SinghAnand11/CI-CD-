install:
	pip install --upgrade pip &&\
        	pip install -r requirements.txt

format:
	black *.py

train:
	python 5083.py

eval:
	echo "## Model Metrics" > readme.md
	cat metrics.txt >> readme.md
   
	echo '\n## Confusion Matrix Plot' >> readme.md
	echo '![Confusion Matrix](model_results.png)' >> readme.md
   
	cml comment create readme.md
