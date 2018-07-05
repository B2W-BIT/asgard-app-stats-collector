import asynctest
from status_collector import get_slave_ip_list
from status_collector import get_slave_statistics
from status_collector import send_slave_statistics_to_queue
from aioresponses import aioresponses

slaves = {
    "slaves": [{
        "id": "90ba2028-fed0-4f19-a2b1-cb35baf9b2cd-S0",
        "hostname": "10.0.111.32",
        "port": 5051,
        "attributes": {
            "dc": "bit",
            "owner": "sieve",
            "mesos": "slave",
            "workload": "general"
        },
        "pid": "slave(1)@10.168.200.94:5051",
        "registered_time": 1528216448.5751
    }, {
        "id": "90ba2028-fed0-4f19-a2b1-cb35baf9b2cd-S0",
        "hostname": "10.0.111.33",
        "port": 5051,
        "attributes": {
            "dc": "bit",
            "owner": "sieve",
            "mesos": "slave",
            "workload": "general"
        },
        "pid": "slave(1)@10.168.200.94:5051",
        "registered_time": 1528216448.5751
    }, {
        "id": "90ba2028-fed0-4f19-a2b1-cb35baf9b2cd-S0",
        "hostname": "10.0.111.34",
        "port": 5051,
        "attributes": {
            "dc": "bit",
            "owner": "sieve",
            "mesos": "slave",
            "workload": "general"
        },
        "pid": "slave(1)@10.168.200.94:5051",
        "registered_time": 1528216448.5751
    }]
}

slave_statistics_response_mock = [{
    "executor_id":
    "sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
    "executor_name":
    "Command Executor (Task: sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430) (Command: NO EXECUTABLE)",
    "framework_id":
    "27b52920-3899-4b90-a1d6-bf83a87f3612-0000",
    "source":
    "sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
    "statistics": {
        "cpus_limit": 8.25,
        "cpus_nr_periods": 769021,
        "cpus_nr_throttled": 1046,
        "cpus_system_time_secs": 34501.45,
        "cpus_throttled_time_secs": 352.597023453,
        "cpus_user_time_secs": 96348.84,
        "mem_anon_bytes": 4845449216,
        "mem_file_bytes": 260165632,
        "mem_limit_bytes": 7650410496,
        "mem_mapped_file_bytes": 7159808,
        "mem_rss_bytes": 5105614848,
        "timestamp": 1388534400.0
    }
}]

slave_statistics_response_mock_without_all_fields = [{
    "executor_id":
    "sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
    "executor_name":
    "Command Executor (Task: sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430) (Command: NO EXECUTABLE)",
    "framework_id":
    "27b52920-3899-4b90-a1d6-bf83a87f3612-0000",
    "source":
    "sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
    "statistics": {
        "cpus_limit": 8.25,
        "cpus_system_time_secs": 34501.45,
        "cpus_user_time_secs": 96348.84,
        "mem_limit_bytes": 7650410496,
        "mem_rss_bytes": 5105614848,
        "timestamp": 1388534400.0
    }
}]

slave_statistics_response_mock_multiple_tasks = [{
    "executor_id":
    "sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
    "executor_name":
    "Command Executor (Task: sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430) (Command: NO EXECUTABLE)",
    "framework_id":
    "27b52920-3899-4b90-a1d6-bf83a87f3612-0000",
    "source":
    "sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
    "statistics": {
        "cpus_limit": 8.25,
        "cpus_nr_periods": 769021,
        "cpus_nr_throttled": 1046,
        "cpus_system_time_secs": 34501.45,
        "cpus_throttled_time_secs": 352.597023453,
        "cpus_user_time_secs": 96348.84,
        "mem_anon_bytes": 4845449216,
        "mem_file_bytes": 260165632,
        "mem_limit_bytes": 7650410496,
        "mem_mapped_file_bytes": 7159808,
        "mem_rss_bytes": 5105614848,
        "timestamp": 1388534400.0
    }
}, {
    "executor_id":
    "sieve2_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
    "executor_name":
    "Command Executor (Task: sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430) (Command: NO EXECUTABLE)",
    "framework_id":
    "27b52920-3899-4b90-a1d6-bf83a87f3612-0000",
    "source":
    "sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
    "statistics": {
        "cpus_limit": 8.25,
        "cpus_nr_periods": 769021,
        "cpus_nr_throttled": 1046,
        "cpus_system_time_secs": 34501.45,
        "cpus_throttled_time_secs": 352.597023453,
        "cpus_user_time_secs": 96348.84,
        "mem_anon_bytes": 4845449216,
        "mem_file_bytes": 260165632,
        "mem_limit_bytes": 7650410496,
        "mem_mapped_file_bytes": 7159808,
        "mem_rss_bytes": 5105614848,
        "timestamp": 1388534400.0
    }
}]


class FecthMasterTest(asynctest.TestCase):
    async def test_get_slaves_ips_list(self):
        with aioresponses() as m:
            m.get('http://10.11.43.96:5050/slaves', payload=slaves)
            slave_ips = await get_slave_ip_list("10.11.43.96")
        self.assertEquals(
            slave_ips,
            ["10.0.111.32:5051", "10.0.111.33:5051", "10.0.111.34:5051"])

    async def test_slave_exists_with_all_fields(self):
        with aioresponses() as m:
            m.get(
                'http://10.0.111.32:5051/monitor/statistics.json',
                payload=slave_statistics_response_mock)
            slave_statistics = await get_slave_statistics("10.0.111.32:5051")
            expected_result = [{
                "appname":
                "/sieve/captura/kirby/powerup",
                "task_name":
                "sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
                "cpu_throttled_percentage":
                0.2694659854808117,
                "memory_usage_percentage":
                66.73648231907895,
                "cpus_limit":
                8.25,
                "cpus_nr_periods":
                769021,
                "cpus_nr_throttled":
                1046,
                "cpus_system_time_secs":
                34501.45,
                "cpus_throttled_time_secs":
                352.597023453,
                "cpus_user_time_secs":
                96348.84,
                "mem_anon_bytes":
                4845449216,
                "mem_file_bytes":
                260165632,
                "mem_limit_bytes":
                7650410496,
                "mem_mapped_file_bytes":
                7159808,
                "mem_rss_bytes":
                5105614848,
                "timestamp":
                1388534400.0
            }]
            self.assertEquals(slave_statistics, expected_result)

    async def test_slave_exists_without_all_fields(self):
        with aioresponses() as m:
            m.get(
                'http://10.0.111.32:5051/monitor/statistics.json',
                payload=slave_statistics_response_mock_without_all_fields)
            slave_statistics = await get_slave_statistics("10.0.111.32:5051")
            expected_result = [{
                "appname":
                "/sieve/captura/kirby/powerup",
                "task_name":
                "sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
                "memory_usage_percentage":
                66.73648231907895,
                "cpus_limit":
                8.25,
                "cpus_system_time_secs":
                34501.45,
                "cpus_user_time_secs":
                96348.84,
                "mem_limit_bytes":
                7650410496,
                "mem_rss_bytes":
                5105614848,
                "timestamp":
                1388534400.0
            }]
            self.assertEquals(slave_statistics, expected_result)

    async def test_get_slave_returns_list_of_tasks(self):
        self.maxDiff = None
        with aioresponses() as m:
            m.get(
                'http://10.0.111.32:5051/monitor/statistics.json',
                payload=slave_statistics_response_mock_multiple_tasks)
            slave_statistics = await get_slave_statistics("10.0.111.32:5051")
            expected_result = [{
                "appname":
                "/sieve/captura/kirby/powerup",
                "task_name":
                "sieve_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
                "cpu_throttled_percentage":
                0.2694659854808117,
                "memory_usage_percentage":
                66.73648231907895,
                "cpus_limit":
                8.25,
                "cpus_nr_periods":
                769021,
                "cpus_nr_throttled":
                1046,
                "cpus_system_time_secs":
                34501.45,
                "cpus_throttled_time_secs":
                352.597023453,
                "cpus_user_time_secs":
                96348.84,
                "mem_anon_bytes":
                4845449216,
                "mem_file_bytes":
                260165632,
                "mem_limit_bytes":
                7650410496,
                "mem_mapped_file_bytes":
                7159808,
                "mem_rss_bytes":
                5105614848,
                "timestamp":
                1388534400.0
            }, {
                "appname":
                "/sieve2/captura/kirby/powerup",
                "task_name":
                "sieve2_captura_kirby_powerup.947f6124-762a-11e8-b78b-c678b0156430",
                "cpu_throttled_percentage":
                0.2694659854808117,
                "memory_usage_percentage":
                66.73648231907895,
                "cpus_limit":
                8.25,
                "cpus_nr_periods":
                769021,
                "cpus_nr_throttled":
                1046,
                "cpus_system_time_secs":
                34501.45,
                "cpus_throttled_time_secs":
                352.597023453,
                "cpus_user_time_secs":
                96348.84,
                "mem_anon_bytes":
                4845449216,
                "mem_file_bytes":
                260165632,
                "mem_limit_bytes":
                7650410496,
                "mem_mapped_file_bytes":
                7159808,
                "mem_rss_bytes":
                5105614848,
                "timestamp":
                1388534400.0
            }]
            self.assertEquals(slave_statistics, expected_result)

    async def test_slave_dont_exists(self):
        with aioresponses() as m:
            with self.assertRaises(Exception):
                m.get(
                    'http://10.0.111.32:5051/monitor/statistics.json',
                    exception=Exception("Invalid slave ip."))
                slave_statistics = await get_slave_statistics(
                    "10.0.111.32:5051")

    async def test_putting_slave_statistics_on_rabbitMQ(self):
        self.maxDiff = None
        with aioresponses() as m:
            m.get('http://10.11.43.96:5050/slaves', payload=slaves)
            slave_ips = await get_slave_ip_list("10.11.43.96")
            m.get(
                f'http://{slave_ips[0]}/monitor/statistics.json',
                payload=slave_statistics_response_mock)
            slave_statistics = await get_slave_statistics(slave_ips[0])
            queue = asynctest.mock.CoroutineMock(
                put=asynctest.mock.CoroutineMock(),
                connect=asynctest.mock.CoroutineMock())
            await send_slave_statistics_to_queue(slave_statistics, queue)
        self.assertEquals([
            asynctest.mock.call(
                body=slave_statistics[0], routing_key="teste.viniciusLouzada")
        ], queue.put.await_args_list)

    async def test_putting_slave_multiple_tasks_statistics_on_rabbitMQ(self):
        self.maxDiff = None
        with aioresponses() as m:
            m.get('http://10.11.43.96:5050/slaves', payload=slaves)
            slave_ips = await get_slave_ip_list("10.11.43.96")
            m.get(
                f'http://{slave_ips[0]}/monitor/statistics.json',
                payload=slave_statistics_response_mock_multiple_tasks)
            slave_statistics = await get_slave_statistics(slave_ips[0])
            queue = asynctest.mock.CoroutineMock(
                put=asynctest.mock.CoroutineMock(),
                connect=asynctest.mock.CoroutineMock())
        await send_slave_statistics_to_queue(slave_statistics, queue)
        self.assertEquals([
            asynctest.mock.call(
                body=slave_statistics[0], routing_key="teste.viniciusLouzada"),
            asynctest.mock.call(
                body=slave_statistics[1], routing_key="teste.viniciusLouzada")
        ], queue.put.await_args_list)
