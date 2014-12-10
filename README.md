Demo of Docker and docker-py
============================

This demo is designed to be used with a (virtual) ubuntu machine that has previously been set up using the puppet config in repo:

	https://github.com/emilybache/demo-puppet

with class 'docker-demo'

1) create a docker image containing a posgres db server and the database 'booktown'

	cd myappdb
	./build.sh

2) start a docker container based on the image

	./run.sh

3) connect to the docker container with pgadmin3 and verify the database is there as expected. Connect to your docker host "localhost.dev" on port 15536. The password is 'postgres'

4) run the dump script against the database:

    cd dump_restore
    ./dump.py --help

Work out what arguments you need by reading the help. The idea is that this is a dump script that you are developing to extract a subset of the production database and sanitize it for testing purposes. The script is only half built and currenly only dumps the schema. Before you develop it any more, you'd like to write automated tests for it

5) run the test fixture for the dump script:

    cd test_dump_restore
    ./test_dump.py

This script uses docker-py to start and stop a docker container with a test database. This test database is supposed to be the same as the production db, but smaller and suitable for testing your dump script.

6) Write an automated test for the dump script using texttest.
