from decimal import Decimal
import decimal
import asyncio
import aiohttp
import aioredis
from aiohttp import ClientTimeout
from easyqueue.async import AsyncQueue, AsyncQueueConsumerDelegate
from status_collector import conf
from asyncworker import App
import time
from aiologger.loggers.json import JsonLogger

timeout_config = ClientTimeout(connect=2, total=5)


async def main():
    conf.cache = await aioredis.create_redis_pool(conf.REDIS_URL, minsize=conf.REDIS_POOL_MIN, maxsize=conf.REDIS_POOL_MAX)
    logger = JsonLogger.with_default_handlers(level=10, flatten=True)
    queue = AsyncQueue(
        conf.STATS_COLLECTOR_RABBITMQ_HOST,
        conf.STATS_COLLECTOR_RABBITMQ_USER,
        conf.STATS_COLLECTOR_RABBITMQ_PWD,
        delegate=Test(),
        virtual_host=conf.STATS_COLLECTOR_RABBITMQ_VHOST)
    await fetch_app_stats(queue, logger)


async def get_slave_ip_list(master_ip):
    try:
        session = aiohttp.ClientSession()
        resp = await session.get(f'http://{master_ip}:5050/slaves', timeout=timeout_config)
        data = await resp.json()
        await session.close()
        return list(map(lambda slave: f'{slave["hostname"]}:{slave["port"]}', data["slaves"]))
    except Exception:
        await session.close()
        raise Exception(f"Invalid master ip {master_ip}.")


def extract_app_name(task):
    return "/" + task["executor_id"].split('.')[0].replace("_", "/")


def extract_task_name(task):
    return task["executor_id"]


def extract_cpu_throttled_percentage(task):
    cpu_system_time = task["statistics"]["cpus_system_time_secs"]
    cpu_user_time = task["statistics"]["cpus_user_time_secs"]
    cpu_throttled_time = task["statistics"]["cpus_throttled_time_secs"]
    return (cpu_throttled_time * 100) / (cpu_system_time + cpu_user_time + cpu_throttled_time)


def extract_memory_usage_percentage(task):
    mem_limit = task["statistics"]["mem_limit_bytes"]
    mem_rss = task["statistics"]["mem_rss_bytes"]
    return (mem_rss * 100) / mem_limit

def round_up(n: Decimal, prec: int=5) -> float:
    return float(n.quantize(Decimal("." + "0" * prec), rounding=decimal.ROUND_UP))


async def build_statistic_for_response(task_now):
    appname = extract_app_name(task_now)
    taskname = extract_task_name(task_now)

    task_before = await conf.cache.get(taskname)
    if not task_before:
        await conf.cache.set(taskname, task_now)
        return None

    now_stats = task_now['statistics']
    before_stats = task_before['statistics']

    await conf.cache.set(taskname, task_now)

    period_secs = Decimal(now_stats['timestamp'] - before_stats['timestamp'])
    cpu_limit = Decimal(now_stats['cpus_limit'])

    cpu_thr_secs = Decimal(now_stats['cpus_throttled_time_secs']) - Decimal(before_stats['cpus_throttled_time_secs'])
    cpu_usr_secs = Decimal(now_stats['cpus_user_time_secs']) - Decimal(before_stats['cpus_user_time_secs'])
    cpu_sys_secs = Decimal(now_stats['cpus_system_time_secs']) - Decimal(before_stats['cpus_system_time_secs'])

    cpu_usr_host_pct = cpu_usr_secs / period_secs * 100
    cpu_sys_host_pct = cpu_sys_secs / period_secs * 100

    mem_bytes = now_stats['mem_rss_bytes']
    mem_pct = Decimal(now_stats['mem_rss_bytes']) / Decimal(now_stats['mem_limit_bytes']) * 100

    cpu_usr_pct = cpu_usr_host_pct / cpu_limit
    cpu_sys_pct = cpu_sys_host_pct / cpu_limit
    cpu_thr_pct = cpu_thr_secs / period_secs * 100
    cpu_pct = (Decimal(cpu_usr_secs) + Decimal(cpu_sys_secs)) / Decimal(cpu_limit) * 100

    data = {
        "stats": {
            "before": task_before['statistics'],
            "now": task_now['statistics']
        },
        "cpu_limit": round_up(cpu_limit, prec=1),
        "host": "10.168.26.167",
        "taskname": taskname,
        "appname": appname,
        "period_secs": round_up(period_secs),
        "cpu_usr_secs": round_up(cpu_usr_secs),
        "cpu_sys_secs": round_up(cpu_sys_secs),
        "cpu_thr_secs": round_up(cpu_thr_secs),
        "mem_bytes": mem_bytes,
        "mem_pct": round_up(mem_pct),
        "cpu_sys_host_pct": round_up(cpu_sys_host_pct),
        "cpu_usr_host_pct": round_up(cpu_usr_host_pct),
        "cpu_usr_pct": round_up(cpu_usr_pct),
        "cpu_sys_pct": round_up(cpu_sys_pct),
        "cpu_pct": round_up(cpu_pct),
        "cpu_thr_pct": round_up(cpu_thr_pct)
    }
    return data


async def get_slave_statistics(slave_ip, logger):
    try:
        session = aiohttp.ClientSession()
        resp = await session.get(f'http://{slave_ip}/monitor/statistics.json', timeout=timeout_config)
        tasks = await resp.json()
        await session.close()
        return list(map(build_statistic_for_response, tasks))
    except Exception as e:
        await session.close()
        raise Exception(f"Invalid slave ip {slave_ip}.")


async def send_slave_statistics_to_queue(slave_statistics, queue, logger):
    await queue.connect()
    for task in slave_statistics:
        await queue.put(
            body=task, routing_key=conf.STATUS_COLLECTOR_RABBITMQ_RK)


async def async_tasks(ip, logger, queue):
    try:
        start = time.time()
        statistics = await get_slave_statistics(ip, logger)
        end = time.time()
        elapsed = end - start
        await logger.info({
                    "action": "fetch_slave_statistics",
                    "slaveIp": ip,
                    "totalTasks": len(statistics),
                    "processTime": elapsed
                })

        await send_slave_statistics_to_queue(statistics, queue, logger)
    except Exception as e:
        await logger.exception(e)

async def fetch_app_stats(queue, logger):
    start = time.time()
    ip_list = await get_slave_ip_list(conf.STATUS_COLLECTOR_MESOS_MASTER_IP)
    await logger.debug({"totalSlaves": len(ip_list), "slaveList": ip_list})
    try:
        tasks = [async_tasks(ip, logger, queue) for ip in ip_list]
        return_values = await asyncio.gather(*tasks, return_exceptions=True)
        end = time.time()
        elapsed = end - start
        await logger.info({
                "action": "fetch_all_slaves_statistics",
                "totalSlaves": len(ip_list),
                "processTime": elapsed
            })
    except Exception as e:
        await logger.exception(e)

class Test(AsyncQueueConsumerDelegate):
    @property
    def queue_name(self) -> str:
        return "nothing"

    async def on_queue_message(self, content, delivery_tag, queue):
        pass
