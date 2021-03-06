build:
	make pilot -s -C ./pilot
	make -s -C ./node

clean:
	make clean -s -C ./pilot
	make clean -s -C ./node

test:
	make test -s -C ./pilot
	make test -s -C ./node

test-image:
	docker build . --file ./node/node/tests/dockerfile --tag test

integration-test:
	make test -s -C integration_tests

containers: clean
	docker build --no-cache -f node.dockerfile -t node .
	docker build --no-cache -f pilot.dockerfile -t pilot .
