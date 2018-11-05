import json
import pytest
import asynctest
from asynctest import mock
from asynctest.mock import CoroutineMock
import aioredis
from aioresponses import aioresponses
from aiologger.loggers.json import JsonLogger

import aiohttp


from status_collector import build_statistic_for_response, conf, get_slave_statistics

@pytest.mark.usefixtures("monitor_statistics_one_task")
@pytest.mark.usefixtures("multiple_reads_monitor_statistics")
@pytest.mark.usefixtures("multiple_reads_monitor_statistics_cfs_off")
@pytest.mark.usefixtures("slave_statistics_multiple_tasks")
class StatsCollectorTest(asynctest.TestCase):

    def setUp(self):
        self.logger = asynctest.Mock(spec=JsonLogger)

    async def test_remove_empty_stats_from_final_list(self):
        """
        O método build_statistic_for_response() deve retornar None caso a task
        em questão não tenha estatisticas anteriores já no cache.

        Os cálculos são feitos apenas quando já temos uma leitura anterior.
        """
        with aioresponses() as m, \
            mock.patch.object(conf, 'cache', CoroutineMock(get=CoroutineMock(), set=CoroutineMock()), create=True) as redis_mock:

            redis_mock.get.side_effect = [self.slave_statistics_multiple_tasks[0], None]
            m.get( 'http://10.0.111.32:5051/monitor/statistics.json', payload=self.slave_statistics_multiple_tasks)

            slave_statistics = await get_slave_statistics( "10.0.111.32:5051", self.logger)
            self.assertEqual(1, len(slave_statistics))
            self.assertEqual("infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020", self.slave_statistics_multiple_tasks[0]["executor_id"])

    async def test_add_task_to_cache_on_first_fetch(self):
        """
        Caso uma task ainda não esteja no cache, não fazemos nada,
        apenas adicionamos essa task no cache

        assert return None
        assert add to cache
        """
        self.maxDiff = None
        task_info = self.monitor_statistics_one_task[0]
        with mock.patch.object(conf, 'cache', CoroutineMock(get=CoroutineMock(), set=CoroutineMock()), create=True) as redis_mock:
            redis_mock.get.return_value = None
            self.assertIsNone(await build_statistic_for_response("10.168.200.55", task_info))
            redis_mock.get.assert_awaited_with(task_info['executor_id'])
            redis_mock.set.assert_awaited_with(task_info['executor_id'], json.dumps(task_info))

    async def test_calculate_metrics_if_task_already_in_cache(self):
        """
        Fazemos todas as contas caso a task em questão já tenha uma entrada
        no cache
        """
        self.maxDiff = None
        task_info_now = self.multuple_reads_monitor_statistics['now']
        task_info_before = self.multuple_reads_monitor_statistics['before']

        with mock.patch.object(conf, 'cache', CoroutineMock(get=CoroutineMock(), set=CoroutineMock()), create=True) as redis_mock:
            redis_mock.get.return_value = json.dumps(task_info_before)
            calculated_metrics = await build_statistic_for_response("10.168.200.55", task_info_now)
            redis_mock.get.assert_awaited_with(task_info_now['executor_id'])
            redis_mock.set.assert_awaited_with(task_info_now['executor_id'], json.dumps(task_info_now))

            expected_results = {
                "stats": {
                    "before": task_info_before['statistics'],
                    "now": task_info_now['statistics']
                },
                **self.multuple_reads_monitor_statistics['expected_result']
            }
            self.assertDictEqual(expected_results, calculated_metrics)

    async def test_calculate_metrics_for_task_without_cfs_enabled(self):
        """
        Devemos ser capazes de de calcular pelo menos as métricas de memória
        para task que estão rodando em agentes sem o CFS enabled.
        """
        self.maxDiff = None
        task_info_now = self.multuple_reads_monitor_statistics_cfs_off['now']
        task_info_before = self.multuple_reads_monitor_statistics_cfs_off['before']

        with mock.patch.object(conf, 'cache', CoroutineMock(get=CoroutineMock(), set=CoroutineMock()), create=True) as redis_mock:
            redis_mock.get.return_value = json.dumps(task_info_before)
            calculated_metrics = await build_statistic_for_response("10.168.200.55", task_info_now)
            redis_mock.get.assert_awaited_with(task_info_now['executor_id'])
            redis_mock.set.assert_awaited_with(task_info_now['executor_id'], json.dumps(task_info_now))

            expected_results = {
                "stats": {
                    "before": task_info_before['statistics'],
                    "now": task_info_now['statistics']
                },
                **self.multuple_reads_monitor_statistics_cfs_off['expected_result']
            }
            self.assertDictEqual(expected_results, calculated_metrics)

    async def test_logs_traceback_if_slave_fetch_fails(self):
        slave_ip = "10.0.1.1:5051"
        with aioresponses() as resp:
            resp.get(f"http://{slave_ip}/monitor/statistics.json", exception=aiohttp.client_exceptions.ClientConnectionError(f"Error connecting to {slave_ip}"))
            with self.assertRaises(Exception):
                expected_result = await get_slave_statistics("10.0.1.1:5051", self.logger)

            self.logger.exception.assert_awaited_with({
                "action": "get_slave_statistics",
                "slave_ip": slave_ip,
                "exception": {
                    "message": "Error connecting to 10.0.1.1:5051",
                    "type": "ClientConnectionError",
                    "traceback": mock.ANY
                }
            })

