#!/bin/bash
sleep 2

echo "starting database with PGDATA: $PGDATA"
gosu postgres postgres -d $PGDATA &
# wait for postgres to start
sleep 2 
echo "adding database booktown"
psql --no-password -h 127.0.0.1 -p 5432 --username=postgres --dbname=postgres -c "CREATE DATABASE \"booktown\" ENCODING='UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' TEMPLATE=template0;"
psql --no-password -h 127.0.0.1 -p 5432 --single-transaction --username=postgres --dbname=booktown  -f /tmp_data/booktown.sql


