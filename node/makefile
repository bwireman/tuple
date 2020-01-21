LINT-REQS = .lint-reqs
TEST-REQS = .test-reqs
BLACK-REQS = .black-reqs
UWSGI-REQS = .uwsgi-reqs

export FLASK_APP = ./node/server.py

env:
	python3 -m venv env
	env/bin/pip install -r requirements.txt

clean:
	rm -rf *.pyc env $(LINT-REQS) $(TEST-REQS) $(BLACK-REQS) $(UWSGI-REQS) .pytest_cache __pycache__ node/containers/__pycache__ node/helpers/__pycache__ node/tests/__pycache__ node/api/__pycache__

$(LINT-REQS): env
	env/bin/pip install flake8 > $(LINT-REQS)

$(TEST-REQS): env
	env/bin/pip install pytest > $(TEST-REQS)

$(BLACK-REQS): env
	env/bin/pip install black > $(BLACK-REQS)

$(UWSGI-REQS): env
	env/bin/pip install uwsgi > $(UWSGI-REQS)

.PHONY: lint
lint: $(LINT-REQS)
	env/bin/flake8 . --exclude=./env --count --show-source --statistics
	env/bin/flake8 . --exclude=./env --count --exit-zero --max-complexity=10 --statistics

.PHONY: format
format: $(BLACK-REQS)
	env/bin/black .

.PHONY: test
test: $(TEST-REQS)
	env/bin/pytest ./node/tests

serve:
	env/bin/flask run

.PHONY: uwsgi
uwsgi: $(UWSGI-REQS)
	env/bin/uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi -H env/