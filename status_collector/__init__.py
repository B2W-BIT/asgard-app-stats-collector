import aiohttp
import asyncio
from easyqueue.async import AsyncQueue, AsyncQueueConsumerDelegate


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
    session = aiohttp.ClientSession()
    try:
        resp = await session.get(f'http://{slave_ip}/monitor/statistics.json')
        data = await resp.json()
        if data[0]["statistics"].get("cpus_throttled_time_secs") is not None:
            app_name = data[0]["executor_id"].split('.')[0]
            app_name = app_name.replace("_", "/")
            app_name = "/" + app_name
            task_name = data[0]["executor_id"]
            cpu_system_time = data[0]["statistics"]["cpus_system_time_secs"]
            cpu_user_time = data[0]["statistics"]["cpus_user_time_secs"]
            cpu_throttled_time = data[0]["statistics"][
                "cpus_throttled_time_secs"]
            cpu_throttled_time_percentage = (cpu_throttled_time * 100) / (
                cpu_system_time + cpu_user_time)
            mem_limit = data[0]["statistics"]["mem_limit_bytes"]
            mem_rss = data[0]["statistics"]["mem_rss_bytes"]
            mem_usage_percentage = (mem_rss * 100) / mem_limit
            result = {
                "appname": app_name,
                "task_name": task_name,
                "cpu_throttled_percentage": cpu_throttled_time_percentage,
                "memory_usage_percentage": mem_usage_percentage,
                **data[0]["statistics"]
            }
        else:
            app_name = data[0]["executor_id"].split('.')[0]
            app_name = app_name.replace("_", "/")
            app_name = "/" + app_name
            task_name = data[0]["executor_id"]
            mem_limit = data[0]["statistics"]["mem_limit_bytes"]
            mem_rss = data[0]["statistics"]["mem_rss_bytes"]
            mem_usage_percentage = (mem_rss * 100) / mem_limit
            result = {
                "appname": app_name,
                "task_name": task_name,
                "memory_usage_percentage": mem_usage_percentage,
                **data[0]["statistics"]
            }
        await session.close()
        return result
    except Exception:
        await session.close()
        raise Exception("Invalid slave ip.")


async def send_slave_statistics_to_queue(slave_statistics, queue):
    await queue.connect()
    await queue.put(body=slave_statistics, routing_key="teste.viniciusLouzada")


class Test(AsyncQueueConsumerDelegate):
    @property
    def queue_name(self) -> str:
        return "nothing"

    async def on_queue_message(self, content, delivery_tag, queue):
        pass


# async def main():
#     Queue = AsyncQueue(
#         "10.168.200.96",
#         "viniciuslouzada",
#         "4RXzFb6fZ0s1E16o",
#         delegate=Test())
#     await Queue.connect()
#     await Queue.put(
#         body={"teste": "teste"}, routing_key="teste.viniciusLouzada")

# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete(main())