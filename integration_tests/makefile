clean:
	docker-compose kill
	docker-compose down
	docker rm -f TEST-1
	docker rm -f TEST-0

test:
	docker build . -f tester.dockerfile -t tester
	docker-compose up --force-recreate -d
	docker run --network integration_tests_default tester
	make clean
