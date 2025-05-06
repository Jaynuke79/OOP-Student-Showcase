TEST = pytest
PLANTUML = java -jar ~/plantuml.jar
TEST_ARGS = -s --verbose --color=yes
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports
STYLE_CHECK = flake8
STYLE_FIX = autopep8 --in-place --recursive --aggressive --aggressive .
<<<<<<<<< Temporary merge branch 1
COVERAGE = python -m pytest

.PHONY: all
all: check-style check-type fix-style run-test-coverage clean
=========
COVERAGE = python3 -m pytest --cov-config=.coveragerc
DOCS = ./docs

.PHONY: all
all: check-style check-type fix-style run-test-coverage create-uml clean
>>>>>>>>> Temporary merge branch 2
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
<<<<<<<<< Temporary merge branch 1
	$(COVERAGE) -v --cov-report=html:. --cov-report=term --cov=. .
=========
	$(COVERAGE) -v --cov=. --cov-report=html:$(DOCS)/py-cov --cov-report=term .

.PHONY: create-cov-report
create-cov-report:
	pytest --verbose --color=yes --cov --cov-report term --cov-report=html:$(DOCS)/py-cov tests/
	@echo "Cover report has been created in $(DOCS)/py-cov folder"

unittest:
	$(PYTHON) -m pytest -v

.PHONY: create-uml
create-uml:
# use shell command which to check if java is installed and is in the $PATH
ifeq ($(shell which java), )
	$(error "No java found in $(PATH). Install java to run plantuml")
endif

ifeq ($(wildcard ~/plantuml.jar), )
	@echo "Downloading plantuml.jar"
	curl -L -o ~/plantuml.jar https://sourceforge.net/projects/plantuml/files/plantuml.jar/download
endif
	$(PLANTUML) plantumls/board.puml
	$(PLANTUML) plantumls/boardPiece.puml
	$(PLANTUML) plantumls/event_classes.puml
	$(PLANTUML) plantumls/pieceClasses.puml
	@echo "UML diagrams created and saved in uml folder"
>>>>>>>>> Temporary merge branch 2

.PHONY: clean
clean:
	# remove all caches recursively
	rm -rf `find . -type d -name __pycache__` # remove all pycache
	rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	rm -rf `find . -name .coverage` # remove all coverage cache 