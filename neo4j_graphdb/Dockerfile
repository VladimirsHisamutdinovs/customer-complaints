FROM neo4j:latest

COPY init_neo4j.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/init_neo4j.sh
