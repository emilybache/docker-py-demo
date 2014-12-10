#!/usr/bin/env python
"Make a dump of the production database"

import sys
assert sys.version_info.minor >= 7 and sys.version_info.major == 2, "this script needs at least version 2.7 of python"

import argparse, datetime, os, shutil
import subprocess, stat

class DbWrapper:
    def __init__(self, db_host, db_port, database):
        self.db_host = db_host
        self.db_port = db_port
        self.database = database

    def host_connection_args(self):
        args = ["--no-password"]
        if not self.db_port == "5432":
            args += ["-p", self.db_port]
        if not self.db_host == "localhost":
            args += ["-h", self.db_host]
        return args

    def db_connection_args(self):
        return self.host_connection_args() + ["-d", self.database, "-U", "postgres"]

    def execute_sql(self, sql):
        return subprocess.check_output(["psql"] + self.db_connection_args() + ["--command", sql])

    def execute_sql_file(self, filename):
        return subprocess.check_output(["psql"] + self.db_connection_args() + ["--file", filename])

    def execute_dump_schema(self, filename, format):
        return subprocess.check_output(["pg_dump", "-U", "postgres"] + self.host_connection_args() +
                                       ["-i", "--schema-only", "--format={}".format(format),
                                        "--file", filename, "-n", "public", self.database])


def main(subject, db_host, db_port, database, output_dir, keep_dump_folder):
    start = datetime.datetime.now()
    db = DbWrapper(db_host, db_port, database)
    dumpname = "dbdump_{}".format(datetime.datetime.now().date().isoformat())
    dump_dir = _prepare_dump_dir(output_dir, dumpname)
    _dump_schema(db, os.path.join(dump_dir, "schema_plain.sql"))
    _dump_subject(db, subject)
        
    print ("dump taken, took {}".format(datetime.datetime.now() - start))
    _compress_dump(output_dir, dumpname, keep_dump_folder)
    print "Dump created successfully in folder {} ".format(output_dir)

    

def _prepare_dump_dir(output_dir, dumpname):
    dump_dir = os.path.join(output_dir, dumpname)
    if os.path.exists(dump_dir):
        shutil.rmtree(dump_dir)
    os.makedirs(dump_dir)
    return dump_dir

def _dump_schema(db, filename):
    print db.execute_dump_schema(filename, 'plain')
    print "schema dumped."

def _dump_subject(db, subject):
    print "here I would like to dump all the database contents, but only books with subject {}".format(subject)

def _compress_dump(output_dir, dumpname, keep_dump_folder):
    output_dir = os.path.abspath(output_dir)
    dumpfile = os.path.join(output_dir, "{}.tgz".format(dumpname))
    cmd = ["tar", "zcvf", dumpfile, "-C", output_dir, dumpname]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print p.stdout.read()
    if not keep_dump_folder:
        shutil.rmtree(os.path.join(output_dir, dumpname))
        generated = os.path.join(output_dir, "generated")
        if os.path.exists(generated):
            shutil.rmtree(generated)
    return dumpfile

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="make a dump of the booktown databases")
    parser.add_argument('--subject', default=2, help="the subject of the books to dump")
    parser.add_argument('--db-host', default="localhost", help="database hostname")
    parser.add_argument('--db-port', '-p', default="5432", help="database port")
    parser.add_argument('--database', default="booktown", help="name of the database to dump")
    parser.add_argument('--output-dir', default="/tmp", help="output dumps to this directory")
    parser.add_argument('--keep-dump-folder', default=False, action='store_true', help="Don't delete temporary files")

    parsed_args = parser.parse_args()
    args_as_dict = vars(parsed_args) # convert Namespace object to python dictionary

    print "will dump messages for subject {subject}".format(**args_as_dict)
    main(**args_as_dict)    
    
