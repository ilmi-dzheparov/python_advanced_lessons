FROM postgres:14

COPY postgresql.conf /etc/postgresql/postgresql.conf

ENTRYPOINT ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
