FROM confluentinc/cp-kafka-connect:7.5.3

# Switch to root to install connector and create directories
USER root

# Install the Confluent Cassandra Connector from Confluent Hub
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-cassandra:2.0.0 || \
    confluent-hub install --no-prompt confluentinc/kafka-connect-cassandra:latest

# Create a directory for connector configs to be mounted
RUN mkdir -p /connectors && chown appuser:appuser /connectors

# Switch back to the non-root user
USER appuser

ENV CONNECT_PLUGIN_PATH=/usr/share/java,/usr/share/confluent-hub-components,/opt/connect-plugins

