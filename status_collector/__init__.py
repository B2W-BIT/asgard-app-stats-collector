import traceback
import sys
import json
from decimal import Decimal
import decimal
import asyncio
import aiohttp
import aioredis
from aiohttp import ClientTimeout
from easyqueue import AsyncQueue, AsyncQueueConsumerDelegate
from status_collector import conf
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


async def get_slave_ip_list(master_ip, logger):
    try:
        session = aiohttp.ClientSession()
        resp = await session.get(f'http://{master_ip}:5050/slaves', timeout=timeout_config)
        data = await resp.json()
        await session.close()
        return list(map(lambda slave: f'{slave["hostname"]}:{slave["port"]}', data["slaves"]))
    except Exception as e:
        await session.close()
        await logger.exception({
            "action": "get_slave_ip_list",
            "exception": {
                "message": str(e),
                "traceback": traceback.format_exc(),
                "type": sys.exc_info()[0].__name__,
            },
            "master_ip": master_ip
        })
        raise e

def extract_app_name(task):
    app_name_with_namespace = task["executor_id"].rsplit(".", 1)[0]
    return "/" + app_name_with_namespace.replace("_", "/")


def extract_task_name(task):
    return task["executor_id"]


def round_up(n: Decimal, prec: int=5) -> float:
    return float(n.quantize(Decimal("." + "0" * prec), rounding=decimal.ROUND_UP))


async def build_statistic_for_response(slave_ip, task_now):
    appname = extract_app_name(task_now)
    taskname = extract_task_name(task_now)

    task_before = await conf.cache.get(taskname)
    if not task_before:
        await conf.cache.set(taskname, json.dumps(task_now))
        return None

    task_before = json.loads(task_before)

    now_stats = task_now['statistics']
    before_stats = task_before['statistics']

    await conf.cache.set(taskname, json.dumps(task_now))

    period_secs = Decimal(now_stats['timestamp'] - before_stats['timestamp'])
    cpu_limit_raw = Decimal(str(now_stats['cpus_limit']))
    cpu_limit = cpu_limit_raw - Decimal("0.1")

    cpu_thr_secs = Decimal(now_stats.get('cpus_throttled_time_secs', 0)) - Decimal(before_stats.get('cpus_throttled_time_secs', 0))
    cpu_usr_secs = Decimal(now_stats['cpus_user_time_secs']) - Decimal(before_stats['cpus_user_time_secs'])
    cpu_sys_secs = Decimal(now_stats['cpus_system_time_secs']) - Decimal(before_stats['cpus_system_time_secs'])

    cpu_usr_host = cpu_usr_secs / period_secs
    cpu_sys_host = cpu_sys_secs / period_secs

    cpu_usr_host_pct = cpu_usr_host * 100
    cpu_sys_host_pct = cpu_sys_host * 100

    mem_bytes = now_stats['mem_rss_bytes']
    mem_pct = Decimal(now_stats['mem_rss_bytes']) / Decimal(now_stats['mem_limit_bytes']) * 100

    cpu_usr_pct = cpu_usr_host_pct / cpu_limit
    cpu_sys_pct = cpu_sys_host_pct / cpu_limit
    cpu_thr_pct = cpu_thr_secs / period_secs * 100
    cpu_pct = (Decimal(cpu_usr_host) + Decimal(cpu_sys_host)) / Decimal(cpu_limit) * 100
    cpu_host_pct = cpu_usr_host_pct + cpu_sys_host_pct

    data = {
        "timestamp": now_stats['timestamp'],
        "cpu_limit": round_up(cpu_limit, prec=1),
        "cpu_limit_raw": round_up(cpu_limit_raw, prec=1),
        "host": slave_ip,
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
        "cpu_thr_pct": round_up(cpu_thr_pct),
        "cpu_pct": round_up(cpu_pct),
        "cpu_host_pct": round_up(cpu_host_pct)
    }

    # Para podermos diferencias tasks que não possuem os dados
    # necessários para calcular o throttling
    if "cpus_throttled_time_secs" not in now_stats:
        del data["cpu_thr_secs"]
        del data["cpu_thr_pct"]

    if conf.STATS_COLLECTOR_INCLUDE_RAW_METRICS:
        data["stats"] = {
            "before": task_before['statistics'],
            "now": task_now['statistics']
        }

    return data


async def get_slave_statistics(slave_ip, logger):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://{slave_ip}/monitor/statistics.json', timeout=timeout_config) as resp:
                tasks = await resp.json()
                async_tasks = [build_statistic_for_response(slave_ip, task) for task in tasks]
    except Exception as e:
        await logger.exception({
            "action": "get_slave_statistics",
            "exception": {
                "message": str(e),
                "traceback": traceback.format_exc(),
                "type": sys.exc_info()[0].__name__,
            },
            "slave_ip": slave_ip
        })
        raise e

    results = await asyncio.gather(*async_tasks, return_exceptions=True)
    valid_results = []
    for r in results:
        if r and not isinstance(r, Exception):
            valid_results.append(r)
        if isinstance(r, Exception):
            await logger.exception({
                "action": "build_slave_stask_statistics",
                "exception": {
                    "message": str(r),
                    "traceback": traceback.format_tb(r.__traceback__),
                    "type": r.__class__.__name__,
                },
                "slave_ip": slave_ip
            })

    return valid_results


async def send_slave_statistics_to_queue(slave_statistics, queue, logger):
    await queue.connect()
    for task in slave_statistics:
        await queue.put(
            body=task, routing_key=conf.STATS_COLLECTOR_RABBITMQ_RK)


async def async_tasks(ip, logger, queue):
    try:
        start = time.time()
        statistics = await get_slave_statistics(ip, logger)
        end = time.time()
        elapsed = end - start
        if statistics:
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
    ip_list = await get_slave_ip_list(conf.STATS_COLLECTOR_MESOS_MASTER_IP, logger)
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
