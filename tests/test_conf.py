import os
from importlib import reload

import asynctest
from asynctest import mock

import status_collector
from status_collector import conf, main


class ConfTest(asynctest.TestCase):
    async def test_read_redis_configs(self):
        expected_redis_url = "redis://cache.asgard/0"
        with mock.patch.dict(
            os.environ,
            STATS_COLLECTOR_REDIS_URL=expected_redis_url,
            STATS_COLLECTOR_REDIS_POOL_MIN="10",
            STATS_COLLECTOR_REDIS_POOL_MAX="32",
        ), mock.patch.object(
            conf.aioredis, "create_redis_pool"
        ) as create_redis_pool_mock:
            reload(conf)
            self.assertEqual(expected_redis_url, conf.REDIS_URL)
            self.assertEqual(10, conf.REDIS_POOL_MIN)
            self.assertEqual(32, conf.REDIS_POOL_MAX)

    def test_read_rabbitmq_configs(self):

        with mock.patch.dict(
            os.environ,
            STATS_COLLECTOR_RABBITMQ_HOST="rmq.asgard",
            STATS_COLLECTOR_RABBITMQ_USER="guest",
            STATS_COLLECTOR_RABBITMQ_PWD="guest-pwd",
            STATS_COLLECTOR_RABBITMQ_RK="routing_key",
            STATS_COLLECTOR_RABBITMQ_VHOST="vhost",
        ):
            reload(conf)
            self.assertEqual("rmq.asgard", conf.STATS_COLLECTOR_RABBITMQ_HOST)
            self.assertEqual("guest", conf.STATS_COLLECTOR_RABBITMQ_USER)
            self.assertEqual("guest-pwd", conf.STATS_COLLECTOR_RABBITMQ_PWD)
            self.assertEqual("routing_key", conf.STATS_COLLECTOR_RABBITMQ_RK)
            self.assertEqual("vhost", conf.STATS_COLLECTOR_RABBITMQ_VHOST)

    def test_read_mesos_master_address(self):
        expected_mesos_master_ip = "192.168.44.89"
        with mock.patch.dict(
            os.environ, STATS_COLLECTOR_MESOS_MASTER_IP=expected_mesos_master_ip
        ):
            reload(conf)
            self.assertEqual(
                expected_mesos_master_ip, conf.STATS_COLLECTOR_MESOS_MASTER_IP
            )

    def test_read_raw_metrics_configs(self):
        reload(conf)
        self.assertFalse(conf.STATS_COLLECTOR_INCLUDE_RAW_METRICS)

        with mock.patch.dict(
            os.environ, STATS_COLLECTOR_INCLUDE_RAW_METRICS="1"
        ):
            reload(conf)
            self.assertTrue(conf.STATS_COLLECTOR_INCLUDE_RAW_METRICS)

        with mock.patch.dict(
            os.environ, STATS_COLLECTOR_INCLUDE_RAW_METRICS="0"
        ):
            reload(conf)
            self.assertFalse(conf.STATS_COLLECTOR_INCLUDE_RAW_METRICS)

    def test_read_connection_timeout_settings(self):

        with mock.patch.dict(
            os.environ, STATS_CONNECT_TIMEOUT="5", STATS_REQUEST_TIMEOUT="30",
        ):
            reload(conf)
            self.assertEqual(5, conf.STATS_CONNECT_TIMEOUT)
            self.assertEqual(30, conf.STATS_REQUEST_TIMEOUT)
