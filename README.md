# Asgard app stats collector  [![Build Status](https://travis-ci.org/B2W-BIT/asgard-app-stats-collector.svg?branch=master)](https://travis-ci.org/B2W-BIT/asgard-app-stats-collector) [![codecov](https://codecov.io/gh/B2W-BIT/asgard-app-stats-collector/branch/master/graph/badge.svg)](https://codecov.io/gh/B2W-BIT/asgard-app-stats-collector)


Coletor de uso de CPU e RAM para todas tasks do cluster do Asgard.


## Fluxo de coleta

* Conecta no master
* Descobre o IP de **todos** os slaves do cluster
* Conecta em cada slave, no endpoint `/monitor/statistics.json`
* Posta o JSON resultante no RabbitMQ


## Configurações


```
STATS_COLLECTOR_RABBITMQ_HOST: IP do RabbitMQ onde as mensagens serão colocadas;
STATS_COLLECTOR_RABBITMQ_PWD: Senha usada no RabbitMQ
STATS_COLLECTOR_RABBITMQ_USER: Username usado no RabbitMQ
STATS_COLLECTOR_RABBITMQ_VHOST: Virtual Host do RabbitMQ
STATS_COLLECTOR_RABBITMQ_RK: Routing Key usada para depositar as mensagens. O exchange usado é sempre `""`
STATS_COLLECTOR_MESOS_MASTER_IP: IP do meso Master (sem incluir a porta)
STATS_COLLECTOR_REDIS_URL: Url completa para o redis
STATS_COLLECTOR_REDIS_POOL_MIN: Tamanho inicial do pool de coexões com o redis
STATS_COLLECTOR_REDIS_POOL_MAX: Tamanho máximo do pool de conexões com o redis
STATS_COLLECTOR_INCLUDE_RAW_METRICS: [0|1] Default: 0. Indica de os valores brutos, usados nos cálculos também serão incluídos no documento final.
```

## Trabalhos futuros

Migra o código para que consiga se conectar em um cluster de mesos master, ou seja, se alguns dos
masters não responder, vai nos próximos.

Isso significa que vamos usar o `get_option()` que existe na `asgard-api-sdk`.

HOLLOWMAN_MESOS_ADDRESS_N: Lista com IP:PORTA de todos os mesos masters

Exemplo:
```
HOLLOWMAN_MESOS_ADDRESS_0: http://IP1:PORTA1
HOLLOWMAN_MESOS_ADDRESS_1: http://IP2:PORTA2
HOLLOWMAN_MESOS_ADDRESS_2: http://IP3:PORTA3
```

* Escrever mais testes, aumentar a cobertura de testes.
* Tratar melhor casos de errot (ConnectionError, ConnectionTimeout, etc)

