FROM ubuntu:latest

# Instalamos las actualizaciones
RUN apt-get update
RUN apt-get upgrade -y

#Instalamos cliente y servidor de MySQL
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-client mysql-server curl
RUN apt-get install -y inetutils-tools inetutils-ping nano wget
RUN apt-get install -y net-tools
#Se habilita el acceso remoto desde MySQL
RUN sed -i -e"s/^bind-address\s+=\s+127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf


# Se crea el volumen
VOLUME ["/opt/mysql"]

# Añadimos el archivo con la base de datos y las tablas.
ADD ./bbdd.sql /var/db/bbdd.sql

#Añadimos la configuracion estandar
ENV user admin
ENV password admin
ENV url file:/var/db/bbdd.sql
ENV right WRITE

#Ejecutamos el script
ADD ./start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Habilitamos el puerto 3306 de MySQL
EXPOSE 3306


#Iniciamos el motor de MySQL

CMD ["/usr/local/bin/start.sh"]

