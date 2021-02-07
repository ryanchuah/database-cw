FROM mysql/mysql-server

COPY . /var/lib/mysql-files/

WORKDIR /app
