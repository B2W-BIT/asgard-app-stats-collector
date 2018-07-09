import asyncio
from status_collector import conf
from easyqueue.async import AsyncQueue
from status_collector import Test, get_slave_ip_list, get_slave_statistics, send_slave_statistics_to_queue


async def main():
    queue = AsyncQueue(
        conf.STATUS_COLLECTOR_RABBITMQ_HOST,
        conf.STATUS_COLLECTOR_RABBITMQ_USER,
        conf.STATUS_COLLECTOR_RABBITMQ_PWD,
        delegate=Test(),
        virtual_host=conf.STATUS_COLLECTOR_RABBITMQ_VHOST)
    ip_list = await get_slave_ip_list(conf.STATUS_COLLECTOR_MESOS_MASTER_IP)
    for ip in ip_list:
        statistics = await get_slave_statistics(ip)
        await send_slave_statistics_to_queue(statistics, queue)


asyncio.get_event_loop().run_until_complete(main())