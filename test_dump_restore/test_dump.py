#!/usr/bin/env python
"Test fixture for script 'dump.py'. Any arguments you pass this script will be passed on as arguments to that script."

import subprocess, os, sys, time

import docker # if this import fails, run 'sudo pip install docker-py'

# fix the PYTHONPATH
src_dir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))
sys.path.insert(0, src_dir)

dbport = 15546

print "starting docker container"
docker_client = docker.Client(base_url = os.environ["DOCKER_HOST"])
container = docker_client.create_container(image="myappdb:0.5", ports=[5432])
docker_client.start(container=container.get("Id"), port_bindings={5432:dbport})
print "started docker container with id={}".format(container.get("Id"))

try:
    logs = docker_client.logs(container=container.get("Id"), stdout=True, stderr=True, timestamps=False, stream=False)
    print logs
    while not "database system is ready to accept connections" in logs:
        time.sleep(0.5)
        logs = docker_client.logs(container=container.get("Id"), stdout=True, stderr=True, timestamps=False, stream=False)
        print logs

    print "docker container ready to accept connections"
    sys.stdout.flush()

    dump_script = "{}/dump_restore/dump.py".format(src_dir)
    cmd = [dump_script, "--db-host", "dev.localhost", "-p", "{}".format(dbport), "--output-dir", "dumpfiles"] + sys.argv[1:]
    print subprocess.check_output(cmd)
finally:
    # stop bootstrap db docker
    print("stopping docker container")
    docker_client.stop(container=container.get("Id"))
    docker_client.remove_container(container=container.get("Id"))
    print("docker container stopped and removed")