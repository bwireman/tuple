LINT-REQS = .lint-reqs
TEST-REQS = .test-reqs


deps:
	python3 -m venv env
	env/bin/pip install -r requirements.txt

clean:
	rm -rf env $(LINT-REQS) $(TEST-REQS) node/__pycache__ node/containers/__pycache__

$(LINT-REQS):
	env/bin/pip install flake8 > $(LINT-REQS)

$(TEST-REQS):
	env/bin/pip install pytest > $(TEST-REQS)

.PHONY: lint
lint: $(LINT-REQS)
	env/bin/flake8 . --exclude=./env --count --show-source --statistics
	env/bin/flake8 . --exclude=./env --count --exit-zero --max-complexity=10 --statistics

.PHONY: test
test: $(TEST-REQS)
	env/bin/pytest ./tests
