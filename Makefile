TEST = pytest
TEST_ARGS = -s --verbose --color=yes
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports
STYLE_CHECK = flake8
STYLE_FIX = autopep8 --in-place --recursive --aggressive --aggressive .
COVERAGE = python -m pytest

.PHONY: all
all: check-style check-type fix-style run-test-coverage clean
	@echo "All checks passed"

.PHONY: check-type
check-type:
	python3 -m pip install types-requests
	$(TYPE_CHECK) .


.PHONY: check-style
check-style:
	$(STYLE_CHECK) .

.PHONY: fix-style
fix-style:
	$(STYLE_FIX) .

# discover and run all tests
.PHONY: run-test
run-test:
	$(TEST) $(TEST_ARGS) .

.PHONY: run-test-coverage
run-test-coverage:
	$(COVERAGE) -v --cov-report=html:. --cov-report=term --cov=. .

.PHONY: clean
clean:
	# remove all caches recursively
	rm -rf `find . -type d -name __pycache__` # remove all pycache
	rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	rm -rf `find . -name .coverage` # remove all coverage cache 