LINT-REQS = .lint-reqs
TEST-REQS = .test-reqs


deps:
	python3 -m venv env
	env/bin/pip install -r requirements.txt

clean:
	rm -rf env $(LINT-REQS)

$(LINT-REQS):
	env/bin/pip install flake8 black > $(LINT-REQS)

$(TEST-REQS):
	env/bin/pip install pytest > $(TEST-REQS)

.PHONY: lint
lint: $(LINT-REQS)
	flake8 . --exclude=./env --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --exclude=./env --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

.PHONY: test
test: $(TEST-REQS)
	pytest ./tests