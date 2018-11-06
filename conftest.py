import pytest

@pytest.fixture(scope="class")
def monitor_statistics_one_task(request):
    request.cls.monitor_statistics_one_task = [
   {
      "executor_id" : "sleep.c45ca6a6-dddc-11e8-a6bb-0242ac120020",
      "framework_id" : "df63a2f4-a419-430f-8ac0-25c5a9f0c0e0-0000",
      "statistics" : {
         "cpus_nr_periods" : 1859,
         "cpus_throttled_time_secs" : 181.632987694,
         "mem_limit_bytes" : 167772160,
         "cpus_system_time_secs" : 0.77,
         "cpus_user_time_secs" : 2.68,
         "timestamp" : 1541080281.1423,
         "mem_rss_bytes" : 90112,
         "cpus_limit" : 0.11,
         "cpus_nr_throttled" : 1768
      },
      "executor_name" : "Command Executor (Task: sleep.c45ca6a6-dddc-11e8-a6bb-0242ac120020) (Command: sh -c 'while true;\n...')",
      "source" : "sleep.c45ca6a6-dddc-11e8-a6bb-0242ac120020"
   }
]

@pytest.fixture(scope="class")
def multiple_reads_monitor_statistics(request):
    request.cls.multuple_reads_monitor_statistics = {
   "before" : {
      "framework_id" : "df63a2f4-a419-430f-8ac0-25c5a9f0c0e0-0000",
      "source" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020",
      "executor_name" : "Command Executor (Task: stress.0741cf07-dde6-11e8-a6bb-0242ac120020) (Command: sh -c 'stress --cpu 1')",
      "statistics" : {
         "mem_rss_bytes" : 98304,
         "cpus_throttled_time_secs" : 22.17612119,
         "timestamp" : 1541084142.7118,
         "cpus_user_time_secs" : 54.88,
         "cpus_nr_periods" : 755,
         "cpus_limit" : 0.7,
         "mem_limit_bytes" : 167772160,
         "cpus_system_time_secs" : 0.09,
         "cpus_nr_throttled" : 752
      },
      "executor_id" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020"
   },
   "now" : {
      "statistics" : {
         "mem_rss_bytes" : 98304,
         "cpus_limit" : 0.7,
         "cpus_throttled_time_secs" : 26.478199097,
         "cpus_user_time_secs" : 65.43,
         "timestamp" : 1541084157.12885,
         "mem_limit_bytes" : 167772160,
         "cpus_nr_throttled" : 896,
         "cpus_system_time_secs" : 0.09,
         "cpus_nr_periods" : 899
      },
      "executor_id" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020",
      "framework_id" : "df63a2f4-a419-430f-8ac0-25c5a9f0c0e0-0000",
      "source" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020",
      "executor_name" : "Command Executor (Task: stress.0741cf07-dde6-11e8-a6bb-0242ac120020) (Command: sh -c 'stress --cpu 1')"
   },
   "expected_result" : {
      "mem_bytes" : 98304,
      "cpu_usr_secs" : 10.55001,
      "cpu_thr_secs" : 4.30208,
      "cpu_pct" : 121.96208,
      "cpu_host_pct": 73.17725,
      "taskname" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020",
      "cpu_sys_secs" : 0.0,
      "period_secs" : 14.41705,
      "cpu_usr_host_pct" : 73.17725,
      "appname" : "/infra/stress",
      "cpu_limit_raw" : 0.7,
      "cpu_limit" : 0.6,
      "cpu_sys_pct" : 0.0,
      "host" : "10.168.200.55",
      "cpu_usr_pct" : 121.96208,
      "cpu_sys_host_pct" : 0.0,
      "cpu_thr_pct" : 29.84021,
      "mem_pct" : 0.0586,
      "timestamp" : 1541084157.12885
   }
}


@pytest.fixture(scope="class")
def multiple_reads_monitor_statistics_cfs_off(request):
    request.cls.multuple_reads_monitor_statistics_cfs_off = {
   "now" : {
      "statistics" : {
         "mem_limit_bytes" : 1107296256,
         "cpus_system_time_secs" : 2178.139999999,
         "cpus_limit" : 0.4,
         "cpus_user_time_secs" : 6209.66,
         "mem_rss_bytes" : 1063415808,
         "timestamp" : 1541094416.35744
      },
      "source" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020",
      "executor_name" : "Command Executor (Task: stress.0741cf07-dde6-11e8-a6bb-0242ac120020) (Command: sh -c 'stress --cpu 1')",
      "framework_id" : "df63a2f4-a419-430f-8ac0-25c5a9f0c0e0-0000",
      "executor_id" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020"
   },
   "expected_result" : {
      "timestamp" : 1541094416.35744,
      "cpu_usr_host_pct" : 0.79138,
      "cpu_pct" : 2.63791,
      "cpu_host_pct": 0.79138,
      "appname" : "/infra/stress",
      "cpu_sys_secs" : 0.0,
      "cpu_usr_pct" : 2.63791,
      "cpu_sys_pct" : 0.0,
      "cpu_limit" : 0.3,
      "cpu_limit_raw" : 0.4,
      "taskname" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020",
      "mem_pct" : 96.03716,
      "mem_bytes" : 1063415808,
      "cpu_usr_secs" : 0.01001,
      "period_secs" : 1.26363,
      "cpu_sys_host_pct" : 0.0,
      "host" : "10.168.200.55"
   },
   "before" : {
      "framework_id" : "df63a2f4-a419-430f-8ac0-25c5a9f0c0e0-0000",
      "executor_id" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020",
      "executor_name" : "Command Executor (Task: stress.0741cf07-dde6-11e8-a6bb-0242ac120020) (Command: sh -c 'stress --cpu 1')",
      "statistics" : {
         "cpus_system_time_secs" : 2178.139999999,
         "mem_limit_bytes" : 1107296256,
         "mem_rss_bytes" : 1063415808,
         "timestamp" : 1541094415.09381,
         "cpus_user_time_secs" : 6209.65,
         "cpus_limit" : 0.4
      },
      "source" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020"
   }
}

@pytest.fixture(scope="class")
def slave_statistics_multiple_tasks(request):
    request.cls.slave_statistics_multiple_tasks = [
   {
      "source" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020",
      "statistics" : {
         "cpus_throttled_time_secs" : 3.480643122,
         "mem_limit_bytes" : 167772160,
         "cpus_nr_throttled" : 120,
         "mem_rss_bytes" : 98304,
         "cpus_system_time_secs" : 0.07,
         "timestamp" : 1541084079.52051,
         "cpus_nr_periods" : 123,
         "cpus_user_time_secs" : 8.81,
         "cpus_limit" : 0.8
      },
      "executor_name" : "Command Executor (Task: infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020) (Command: sh -c 'stress --cpu 1')",
      "framework_id" : "df63a2f4-a419-430f-8ac0-25c5a9f0c0e0-0000",
      "executor_id" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020"
   },
   {
      "executor_name" : "Command Executor (Task: infra_sleep.c45ca6a6-dddc-11e8-a6bb-0242ac120020) (Command: sh -c 'while true;\n...')",
      "statistics" : {
         "cpus_throttled_time_secs" : 3705.155535528,
         "mem_limit_bytes" : 167772160,
         "cpus_nr_throttled" : 36669,
         "mem_rss_bytes" : 1253376,
         "cpus_system_time_secs" : 20.13,
         "cpus_nr_periods" : 38703,
         "timestamp" : 1541084079.52572,
         "cpus_user_time_secs" : 52.47,
         "cpus_limit" : 0.11
      },
      "executor_id" : "infra_sleep.c45ca6a6-dddc-11e8-a6bb-0242ac120020",
      "framework_id" : "df63a2f4-a419-430f-8ac0-25c5a9f0c0e0-0000",
      "source" : "infra_sleep.c45ca6a6-dddc-11e8-a6bb-0242ac120020"
   }
]

@pytest.fixture(scope="class")
def cpu_limit_valor_com_arredondamento_incorreto(request):
    request.cls.cpu_limit_valor_com_arredondamento_incorreto = {
   "now" : {
      "statistics" : {
         "mem_limit_bytes" : 1107296256,
         "cpus_system_time_secs" : 2178.139999999,
         "cpus_limit" : 0.9,
         "cpus_user_time_secs" : 6209.66,
         "mem_rss_bytes" : 1063415808,
         "timestamp" : 1541094416.35744
      },
      "source" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020",
      "executor_name" : "Command Executor (Task: stress.0741cf07-dde6-11e8-a6bb-0242ac120020) (Command: sh -c 'stress --cpu 1')",
      "framework_id" : "df63a2f4-a419-430f-8ac0-25c5a9f0c0e0-0000",
      "executor_id" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020"
   },
   "expected_result" : {
      "cpu_limit" : 0.9,
   },
   "before" : {
      "framework_id" : "df63a2f4-a419-430f-8ac0-25c5a9f0c0e0-0000",
      "executor_id" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020",
      "executor_name" : "Command Executor (Task: stress.0741cf07-dde6-11e8-a6bb-0242ac120020) (Command: sh -c 'stress --cpu 1')",
      "statistics" : {
         "cpus_system_time_secs" : 2178.139999999,
         "mem_limit_bytes" : 1107296256,
         "mem_rss_bytes" : 1063415808,
         "timestamp" : 1541094415.09381,
         "cpus_user_time_secs" : 6209.65,
         "cpus_limit" : 0.9
      },
      "source" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020"
   }
    }
