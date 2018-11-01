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
      "cpu_pct" : 1507.14286,
      "taskname" : "infra_stress.0741cf07-dde6-11e8-a6bb-0242ac120020",
      "cpu_sys_secs" : 0.0,
      "period_secs" : 14.41705,
      "cpu_usr_host_pct" : 73.17725,
      "appname" : "/infra/stress",
      "cpu_limit" : 0.7,
      "cpu_sys_pct" : 0.0,
      "host" : "10.168.26.167",
      "cpu_usr_pct" : 104.53893,
      "cpu_sys_host_pct" : 0.0,
      "cpu_thr_pct" : 29.84021,
      "mem_pct" : 0.0586
   }
}

