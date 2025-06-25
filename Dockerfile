FROM apache/airflow:2.0.1-python3.8

# Install Java and build dependencies first (required for PySpark)
USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    openjdk-11-jdk \
    build-essential \
    ca-certificates-java && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    update-ca-certificates -f

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Switch back to airflow user for installing Python packages
USER airflow

# Copy and install Python requirements
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt