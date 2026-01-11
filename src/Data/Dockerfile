# Usa a versão oficial e estável do MongoDB (baseada no Ubuntu 22.04 para compatibilidade)
FROM mongo:7.0-jammy

#COPY import.sh /docker-initdb.d/init-import.sh
#RUN chmod +x /docker-initdb.d/init-import.sh
#RUN ./docker-initdb.d/init-import.sh
COPY . /data
VOLUME /data/db
EXPOSE 27017
CMD ["mongod"]
