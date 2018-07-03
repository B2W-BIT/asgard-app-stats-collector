# Asgard app stats collector


Coletor de uso de CPU e RAM para todas tasks do cluster do Asgard.


## Fluxo de coleta

* Conecta no master
* Descobre o IP de **todos** os slaves do cluster
* Conecta em cada slave, no endpoint `/monitor/statistics.json`
* Posta o JSON resultante no RabbitMQ


## Configurações

HOLLOWMAN_MESOS_ADDRESS_N: Lista com IP:PORTA de todos os mesos masters

Exemplo:
HOLLOWMAN_MESOS_ADDRESS_0: IP1
HOLLOWMAN_MESOS_ADDRESS_1: IP2
HOLLOWMAN_MESOS_ADDRESS_2: IP3
