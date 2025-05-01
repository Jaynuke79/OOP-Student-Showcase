# Define tools and arguments
TEST = pytest
TEST_ARGS = -s --verbose --color=yes
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports --explicit-package-bases
STYLE_CHECK = flake8
COVERAGE = python -m pytest --cov=$(SOURCE_DIR)

# Adjust these paths based on your project structure
SOURCE_DIR = /home/cdhockins/OOP-Student-Showcase
TEST_MODULE_DIR = /home/cdhockins/OOP-Student-Showcase/test_modules

.PHONY: all
all: check-style check-type run-test-coverage clean
	@echo "All checks passed"

.PHONY: check-style
check-style:
	$(STYLE_CHECK) $(SOURCE_DIR)

.PHONY: check-type
check-type:
	$(TYPE_CHECK) $(SOURCE_DIR)

.PHONY: run-test
run-test:
	PYTHONPATH=$(SOURCE_DIR) $(TEST) $(TEST_ARGS)

.PHONY: run-test-coverage
run-test-coverage:
	PYTHONPATH=$(SOURCE_DIR) $(COVERAGE) $(TEST_ARGS)

.PHONY: clean
clean:
	# remove all Python and tool-specific cache files
	rm -rf $(shell find . -type d -name '__pycache__')
	rm -rf $(shell find . -type d -name '.pytest_cache')
	rm -rf $(shell find . -type d -name '.mypy_cache')
	rm -rf $(shell find . -type d -name '.hypothesis')
	rm -f .coverage
