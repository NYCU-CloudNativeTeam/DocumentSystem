FROM mysql:8.3

# TODO: using secret
ENV MYSQL_ROOT_PASSWORD=nycu_is_good
ENV MYSQL_USER=document_center
ENV MYSQL_PASSWORD=nycu_is_good

COPY system/db/schema/*.sql /docker-entrypoint-initdb.d

EXPOSE 3306