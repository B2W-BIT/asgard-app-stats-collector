import os
import aioredis

STATS_COLLECTOR_MESOS_MASTER_IP = os.getenv(
    "STATS_COLLECTOR_MESOS_MASTER_IP")

STATS_COLLECTOR_RABBITMQ_HOST = os.getenv("STATS_COLLECTOR_RABBITMQ_HOST")
STATS_COLLECTOR_RABBITMQ_USER = os.getenv("STATS_COLLECTOR_RABBITMQ_USER")
STATS_COLLECTOR_RABBITMQ_PWD = os.getenv("STATS_COLLECTOR_RABBITMQ_PWD")
STATS_COLLECTOR_RABBITMQ_RK = os.getenv("STATS_COLLECTOR_RABBITMQ_RK")
STATS_COLLECTOR_RABBITMQ_VHOST = os.getenv("STATS_COLLECTOR_RABBITMQ_VHOST")
STATS_COLLECTOR_INCLUDE_RAW_METRICS = bool(int(os.getenv("STATS_COLLECTOR_INCLUDE_RAW_METRICS", "0")))

REDIS_URL = os.getenv("STATS_COLLECTOR_REDIS_URL", "redis://127.0.0.1/0")
REDIS_POOL_MIN = int(os.getenv("STATS_COLLECTOR_REDIS_POOL_MIN", 5))
REDIS_POOL_MAX = int(os.getenv("STATS_COLLECTOR_REDIS_POOL_MAX", 10))
