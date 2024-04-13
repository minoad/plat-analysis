.PHONY: build
build:
	pip install -e .

.PHONY: typehint
typehint:
	mypy --ignore-missing-imports plat/

.PHONY: test
test:
	pytest test/

.PHONY: test-coverage
test-coverage:  ## Run tests with coverage
	coverage erase
	coverage run -m pytest
	coverage report -m

.PHONY: lint
lint: lint_pylint lint_flake8 black typehint

.PHONY: lint_pylint
lint_pylint:
	pylint --max-line-length=120 plat/

.PHONY: lint_flake8
lint_flake8:
	flake8 --max-line-length=120 --ignore=E266,E402,F841,F401,E302,E305 .

.PHONY: checklist
checklist: lint typehint test

.PHONY: black
black:
	black -l 120 .

.PHONY: clean
clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
