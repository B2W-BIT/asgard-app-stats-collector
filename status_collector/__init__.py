import aiohttp
import asyncio
from easyqueue.async import AsyncQueue, AsyncQueueConsumerDelegate
from status_collector import conf


async def get_slave_ip_list(master_ip):
    session = aiohttp.ClientSession()
    resp = await session.get(f'http://{master_ip}:5050/slaves')
    data = await resp.json()
    result = []
    for slave in data["slaves"]:
        result.append(f'{slave["hostname"]}:{slave["port"]}')
    await session.close()
    return result


async def get_slave_statistics(slave_ip):
    try:
        session = aiohttp.ClientSession()
        result = []
        resp = await session.get(f'http://{slave_ip}/monitor/statistics.json')
        data = await resp.json()
        for val in data:
            if val["statistics"].get("cpus_throttled_time_secs") is not None:
                app_name = val["executor_id"].split('.')[0]
                app_name = app_name.replace("_", "/")
                app_name = "/" + app_name
                task_name = val["executor_id"]
                cpu_system_time = val["statistics"]["cpus_system_time_secs"]
                cpu_user_time = val["statistics"]["cpus_user_time_secs"]
                cpu_throttled_time = val["statistics"][
                    "cpus_throttled_time_secs"]
                cpu_throttled_time_percentage = (cpu_throttled_time * 100) / (
                    cpu_system_time + cpu_user_time)
                mem_limit = val["statistics"]["mem_limit_bytes"]
                mem_rss = val["statistics"]["mem_rss_bytes"]
                mem_usage_percentage = (mem_rss * 100) / mem_limit
                statistics = {
                    "appname": app_name,
                    "task_name": task_name,
                    "cpu_throttled_percentage": cpu_throttled_time_percentage,
                    "memory_usage_percentage": mem_usage_percentage,
                    **val["statistics"]
                }
                result.append(statistics)
            else:
                app_name = val["executor_id"].split('.')[0]
                app_name = app_name.replace("_", "/")
                app_name = "/" + app_name
                task_name = val["executor_id"]
                mem_limit = val["statistics"]["mem_limit_bytes"]
                mem_rss = val["statistics"]["mem_rss_bytes"]
                mem_usage_percentage = (mem_rss * 100) / mem_limit
                statistics = {
                    "appname": app_name,
                    "task_name": task_name,
                    "memory_usage_percentage": mem_usage_percentage,
                    **val["statistics"]
                }
                result.append(statistics)
        await session.close()
        return result
    except Exception:
        await session.close()
        raise Exception("Invalid slave ip.")


async def send_slave_statistics_to_queue(slave_statistics, queue):
    await queue.connect()
    for task in slave_statistics:
        await queue.put(
            body=task, routing_key=conf.STATUS_COLLECTOR_RABBITMQ_RK)


class Test(AsyncQueueConsumerDelegate):
    @property
    def queue_name(self) -> str:
        return "nothing"

    async def on_queue_message(self, content, delivery_tag, queue):
        pass


async def main():
    queue = AsyncQueue(
        conf.STATUS_COLLECTOR_RABBITMQ_HOST,
        conf.STATUS_COLLECTOR_RABBITMQ_USER,
        conf.STATUS_COLLECTOR_RABBITMQ_PWD,
        delegate=Test())
    ip_list = await get_slave_ip_list(conf.STATUS_COLLECTOR_RABBITMQ_HOST)
    for ip in ip_list:
        statistics = await get_slave_statistics(ip)
        await send_slave_statistics_to_queue(statistics, queue)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())