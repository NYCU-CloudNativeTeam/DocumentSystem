FROM mysql:8.3

# TODO: using secret

COPY system/db/schema/*.sql /docker-entrypoint-initdb.d

EXPOSE 3306
