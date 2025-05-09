FROM flink:1.19.0-scala_2.12-java11

COPY sql-client.sh /opt/sql-client/

RUN mkdir -p /opt/sql-client/lib

RUN wget -P /opt/sql-client/lib https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.2.0-1.19/flink-sql-connector-kafka-3.2.0-1.19.jar; \
    wget -P /opt/sql-client/lib https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.1-1.17/flink-connector-jdbc-3.1.1-1.17.jar; \
    wget -P /opt/sql-client/lib https://repo.maven.apache.org/maven2/org/apache/flink/flink-json/1.17.1/flink-json-1.17.1.jar; \
    wget -P /opt/sql-client/lib https://jdbc.postgresql.org/download/postgresql-42.5.6.jar; \
    wget -P /opt/sql-client/lib https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-avro-confluent-registry/1.19.2/flink-sql-avro-confluent-registry-1.19.2.jar; 


WORKDIR /opt/sql-client
ENV SQL_CLIENT_HOME=/opt/sql-client

COPY docker-entrypoint.sh /opt/sql-client
RUN chmod +x /opt/sql-client/docker-entrypoint.sh 
ENTRYPOINT ["/opt/sql-client/docker-entrypoint.sh"]