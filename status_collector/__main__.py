import asyncio
from status_collector import conf
from easyqueue.async import AsyncQueue
from status_collector import Test, get_slave_ip_list, get_slave_statistics, send_slave_statistics_to_queue, async_tasks, fetch_app_stats
from aiologger.loggers.json import JsonLogger

async def main():
    logger = await JsonLogger.with_default_handlers(level=10, flatten=True)
    queue = AsyncQueue(
        conf.STATUS_COLLECTOR_RABBITMQ_HOST,
        conf.STATUS_COLLECTOR_RABBITMQ_USER,
        conf.STATUS_COLLECTOR_RABBITMQ_PWD,
        delegate=Test(),
        virtual_host=conf.STATUS_COLLECTOR_RABBITMQ_VHOST)
    await fetch_app_stats(queue, logger)


asyncio.get_event_loop().run_until_complete(main())

