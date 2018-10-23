.PHONY: clean
clean:
	find . -name '__pycache__' -exec rm -r {} +
	find . -name '*.pyc' -exec rm {} +
	find . -name '*.pyo' -exec rm {} +
	find . -name '*.log' -exec rm {} +

.PHONY: lint
lint:
	flake8

.PHONY: debug
debug:
	python3 run.py --debug

.PHONY: run
run:
	sudo python3 run.py