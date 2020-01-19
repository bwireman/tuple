build:
	make build -C ./pilot
	make -C ./node

clean:
	make clean -C ./pilot
	make clean -C ./node

test:
	make test -C ./pilot
	make test -C ./node

containers:
	docker build -f node.dockerfile -t node .
	docker build -f pilot.dockerfile -t pilot .
