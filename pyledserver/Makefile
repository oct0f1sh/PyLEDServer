.PHONY: clean
clean:
	find . -name '__pycache__' -exec rm -r {} +
	find . -name '*.pyc' -exec rm {} +
	find . -name '*.pyo' -exec rm {} +
	find . -name '*.log' -exec rm {} +

.PHONY: lint
lint:
	flake8

.PHONY: run-debug
run-debug:
	python run.py --debug

.PHONY: run
run:
	python run.py