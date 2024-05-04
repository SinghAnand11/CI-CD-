install:
	pip install --upgrade pip &&\
        	pip install -r requirements.txt

format:
	black *.py

train:
	python 5083.py

eval:
	echo "## Model Metrics" > report.md
	cat .metrics.txt >> report.md
   
	echo '\n## Confusion Matrix Plot' >> report.md
	echo '![Confusion Matrix](.model_results.png)' >> report.md
   
	cml comment create report.md
