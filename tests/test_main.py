from importlib import reload
import asynctest
from asynctest import mock
from status_collector import conf, main
import status_collector
import os

class MainTest(asynctest.TestCase):

    async def test_main_creates_redis_pool(self):
        expected_redis_url = "redis://cache.asgard/0"
        with mock.patch.dict(os.environ,
                             STATS_COLLECTOR_REDIS_URL=expected_redis_url,
                             STATS_COLLECTOR_REDIS_POOL_MIN="10",
                             STATS_COLLECTOR_REDIS_POOL_MAX="32"), \
                mock.patch.object(status_collector.aioredis, "create_redis_pool") as create_redis_pool_mock, \
                mock.patch.object(status_collector, "fetch_app_stats"):
            reload(conf)
            await main()
            create_redis_pool_mock.assert_awaited_with(expected_redis_url, minsize=10, maxsize=32)
            self.assertTrue(conf.cache)
