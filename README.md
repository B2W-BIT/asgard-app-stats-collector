# Asgard app stats collector  [![Build Status](https://travis-ci.org/B2W-BIT/asgard-app-stats-collector.svg?branch=master)](https://travis-ci.org/B2W-BIT/asgard-app-stats-collector) [![codecov](https://codecov.io/gh/B2W-BIT/asgard-api/branch/master/graph/badge.svg)](https://codecov.io/gh/B2W-BIT/asgard-api)


Coletor de uso de CPU e RAM para todas tasks do cluster do Asgard.


## Fluxo de coleta

* Conecta no master
* Descobre o IP de **todos** os slaves do cluster
* Conecta em cada slave, no endpoint `/monitor/statistics.json`
* Posta o JSON resultante no RabbitMQ


## Configurações


STATUS_COLLECTOR_RABBITMQ_HOST
STATUS_COLLECTOR_RABBITMQ_PWD
STATUS_COLLECTOR_RABBITMQ_USER
STATUS_COLLECTOR_RABBITMQ_VHOST=
STATUS_COLLECTOR_RABBITMQ_RK=
STATUS_COLLECTOR_MESOS_MASTER_IP=


## Trabalhos futuros

Migra o código para que consiga se conectar em um cluster de mesos master, ou seja, se alguns dos
masters não responder, vai nos próximos.

Isso significa que vamos usar o `get_option()` que existe na `asgard-api-sdk`.

HOLLOWMAN_MESOS_ADDRESS_N: Lista com IP:PORTA de todos os mesos masters

Exemplo:
HOLLOWMAN_MESOS_ADDRESS_0: IP1
HOLLOWMAN_MESOS_ADDRESS_1: IP2
HOLLOWMAN_MESOS_ADDRESS_2: IP3


* Escrever mais testes, aumentar a cobertura de testes.
* Tratar melhor casos de errot (ConnectionError, ConnectionTimeout, etc)
* Refatorar o código que monta os documentos com estatísticas de uma slave, remover código duplicado
* Buscar os dados dos slaves com código concorrente. Atualmente o código vai em um slave de cada vez.

