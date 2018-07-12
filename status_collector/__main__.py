import asyncio
from status_collector import conf
from easyqueue.async import AsyncQueue
from status_collector import Test, get_slave_ip_list, get_slave_statistics, send_slave_statistics_to_queue, async_tasks
from aiologger.loggers.json import JsonLogger


async def main():
    logger = await JsonLogger.with_default_handlers(level=10, flatten=True)
    queue = AsyncQueue(
        conf.STATUS_COLLECTOR_RABBITMQ_HOST,
        conf.STATUS_COLLECTOR_RABBITMQ_USER,
        conf.STATUS_COLLECTOR_RABBITMQ_PWD,
        delegate=Test(),
        virtual_host=conf.STATUS_COLLECTOR_RABBITMQ_VHOST)
    ip_list = await get_slave_ip_list(conf.STATUS_COLLECTOR_MESOS_MASTER_IP)
    await logger.debug({"totalSlaves": len(ip_list), "slaveList": ip_list})
    
    try:
        tasks = [async_tasks(ip, logger, queue) for ip in ip_list]
        await asyncio.gather(*tasks)
    except Exception as e:
        await logger.exception(e)


asyncio.get_event_loop().run_until_complete(main())

