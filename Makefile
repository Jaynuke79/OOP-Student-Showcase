PYTHONPATH := $(shell pwd)

test:
	@echo "Running all tests in test_modules/..."
	PYTHONPATH=$(PYTHONPATH) python3 -m unittest discover -s test_modules -p "test_*.py"
