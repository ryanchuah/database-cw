FROM mysql:5.7

COPY . /var/lib/mysql-files/

WORKDIR /app
