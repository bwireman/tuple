LINT-REQS = .lint-reqs


deps:
	python3 -m venv env
	env/bin/pip install -r requirements.txt

clean:
	rm -rf env $(LINT-REQS)

$(LINT-REQS):
	env/bin/pip install flake8 black > $(LINT-REQS)

.PHONY: lint
lint: $(LINT-REQS)
	black .
	flake8 . --exclude=./env
