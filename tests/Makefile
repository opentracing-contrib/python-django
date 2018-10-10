project := django_opentracing

.PHONY: test clean

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

test: clean
	coverage run --source='$(project)' --omit='*_version.py' manage.py test && coverage report -m
