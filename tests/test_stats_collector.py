import pytest
import asynctest
from asynctest import mock
from asynctest.mock import CoroutineMock
import aioredis

from status_collector import build_statistic_for_response, conf

@pytest.mark.usefixtures("monitor_statistics_one_task")
@pytest.mark.usefixtures("multiple_reads_monitor_statistics")
@pytest.mark.usefixtures("multiple_reads_monitor_statistics_cfs_off")
class StatsCollectorTest(asynctest.TestCase):

    def test_remove_empty_stats_from_final_list(self):
        """
        O método build_statistic_for_response() deve retornar None caso a task
        em questão não tenha estatisticas anteriores já no cache.

        Os cálculos são feitos apenas quando já temos uma leitura anterior.
        """
        self.fail()

    async def test_add_task_to_cache_on_first_fetch(self):
        """
        Caso uma task ainda não esteja no cache, não fazemos nada,
        apenas adicionamos essa task no cache

        assert return None
        assert add to cache
        """
        task_info = self.monitor_statistics_one_task[0]
        with mock.patch.object(conf, 'cache', CoroutineMock(get=CoroutineMock(), set=CoroutineMock()), create=True) as redis_mock:
            redis_mock.get.return_value = None
            self.assertIsNone(await build_statistic_for_response(task_info))
            redis_mock.get.assert_awaited_with(task_info['executor_id'])
            redis_mock.set.assert_awaited_with(task_info['executor_id'], task_info)


    async def test_calculate_metrics_if_task_already_in_cache(self):
        """
        Fazemos todas as contas caso a task em questão já tenha uma entrada
        no cache
        """
        self.maxDiff = None
        task_info_now = self.multuple_reads_monitor_statistics['now']
        task_info_before = self.multuple_reads_monitor_statistics['before']

        with mock.patch.object(conf, 'cache', CoroutineMock(get=CoroutineMock(), set=CoroutineMock()), create=True) as redis_mock:
            redis_mock.get.return_value = task_info_before
            calculated_metrics = await build_statistic_for_response("10.168.200.55", task_info_now)
            redis_mock.get.assert_awaited_with(task_info_now['executor_id'])
            redis_mock.set.assert_awaited_with(task_info_now['executor_id'], task_info_now)

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
            redis_mock.get.return_value = task_info_before
            calculated_metrics = await build_statistic_for_response("10.168.200.55", task_info_now)
            redis_mock.get.assert_awaited_with(task_info_now['executor_id'])
            redis_mock.set.assert_awaited_with(task_info_now['executor_id'], task_info_now)

            expected_results = {
                "stats": {
                    "before": task_info_before['statistics'],
                    "now": task_info_now['statistics']
                },
                **self.multuple_reads_monitor_statistics_cfs_off['expected_result']
            }
            self.assertDictEqual(expected_results, calculated_metrics)

    def test_update_cache_after_all_calculations(self):
        """
        Após os cálculos precisamos atualizar os dados do cache com a leitura
        atual da task
        """
        self.fail()

    def test_get_slave_statistics_passa_slave_ip_adiante(self):
        """
        Precisamos passar o slave_ip para a função que calcula as métricas
        """
        self.fail()
