project := django_opentracing

.PHONY: test publish install clean clean-build clean-pyc clean-test build

install:
	pip install -r requirements.txt
	pip install -r requirements-test.txt
	python setup.py install

check-virtual-env:
	@echo virtual-env: $${VIRTUAL_ENV?"Please run in virtual-env"}

bootstrap: check-virtual-env
	pip install -r requirements.txt
	pip install -r requirements-test.txt
	python setup.py develop

clean: clean-build clean-pyc clean-test

clean-build:
	python setup.py clean
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr .cache/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -f .coverage
	rm -f coverage.xml
	rm -fr htmlcov/

lint:
	# Ignore single/double quotes related errors, as Django uses them extensively.
	flake8 --ignore=Q000,Q002 $(project)

test: 
	make -C tests test

build: 
	python setup.py build
