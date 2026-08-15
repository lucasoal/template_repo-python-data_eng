FROM quay.io/astronomer/astro-runtime:13.9.0

USER root

RUN apt-get update && apt-get install -y \
    chromium \
    wget \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p     /usr/local/airflow/include/assets \
    && chmod -R 777 /usr/local/airflow/include/assets \
    && mkdir -p     /usr/local/airflow/tmp \
    && chmod -R 777 /usr/local/airflow/tmp

USER astro