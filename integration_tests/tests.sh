docker run --network container:integration_tests_node_1 appropriate/curl -s --retry 10 --retry-connrefused http://localhost:5000/ 

docker run --network container:integration_tests_pilot_1 appropriate/curl -s --retry 10 --retry-connrefused http://localhost:5001/v0.1/

docker run --network container:integration_tests_node_1 appropriate/curl -s --retry 10 --retry-connrefused -X POST --data '{ "path" : "http://pilot:5001" }' -H "Content-Type: application/json" localhost:5000/register 

docker run --network container:integration_tests_pilot_1 appropriate/curl -s --retry 10 --retry-connrefused http://localhost:5001/v0.1/
