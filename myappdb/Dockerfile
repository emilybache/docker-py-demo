FROM postgres:9.3
MAINTAINER Emily Bache

ENV POSTGRES_PASSWORD postgres

# keep database data actually on the docker image instead of in a VOLUME
ENV PGDATA /data

COPY ./bootstrap.sh /
COPY ./entrypoint.sh /
COPY ./create.sh /
ADD data /tmp_data

RUN /create.sh postgres
RUN /bootstrap.sh
RUN rm -rf /tmp_data

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 5432

CMD ["postgres"]
