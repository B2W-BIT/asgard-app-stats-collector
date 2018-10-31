import asyncio
import aiohttp

import json
import os

agent_ip = os.environ.get("AGENT_IP")


CACHE = {}

def print_json(before, now):
    now_stats = now['statistics']
    before_stats = before['statistics']
    period_secs = now_stats['timestamp'] - before_stats['timestamp']
    cpu_limit = now_stats['cpus_limit']

    cpu_thr_secs = now_stats['cpus_throttled_time_secs'] - before_stats['cpus_throttled_time_secs']
    cpu_usr_secs = now_stats['cpus_user_time_secs'] - before_stats['cpus_user_time_secs']
    cpu_sys_secs = now_stats['cpus_system_time_secs'] - before_stats['cpus_system_time_secs']

    cpu_usr_host_pct = cpu_usr_secs / period_secs * 100
    cpu_sys_host_pct = cpu_sys_secs / period_secs * 100

    mem_bytes = now_stats['mem_rss_bytes']
    mem_pct = now_stats['mem_rss_bytes'] / now_stats['mem_limit_bytes'] * 100

    cpu_usr_pct = cpu_usr_host_pct / cpu_limit
    cpu_sys_pct = cpu_sys_host_pct / cpu_limit
    cpu_thr_pct = cpu_thr_secs / period_secs * 100
    cpu_pct = (cpu_usr_secs + cpu_sys_secs) / cpu_limit * 100

    data = {
        "stats": {
            "before": before['statistics'],
            "now": now['statistics']
        },
        "cpu_limit": cpu_limit,
        "host": agent_ip,
        "taskname": now['source'],
        "appname": "/infra/stress",
        "period_secs": period_secs,
        "cpu_usr_secs": cpu_usr_secs,
        "cpu_sys_secs": cpu_sys_secs,
        "cpu_thr_secs": cpu_thr_secs,
        "mem_bytes": mem_bytes,
        "mem_pct": mem_pct,
        "cpu_sys_host_pct": cpu_sys_host_pct,
        "cpu_usr_host_pct": cpu_usr_host_pct,
        "cpu_usr_pct": cpu_usr_pct,
        "cpu_sys_pct": cpu_sys_pct,
        "cpu_pct": cpu_pct,
        "cpu_thr_pct": cpu_thr_pct
    }

    print(json.dumps(data, indent=2))


async def main():
    while True:
        s = aiohttp.ClientSession()
        r = await s.get(f"http://{agent_ip}:5051/monitor/statistics.json")
        data = await r.json()
        await s.close()
        for task_data in data:
            task_name = task_data['source']
            if task_name not in CACHE:
                CACHE[task_name] = task_data
                continue
            before = CACHE[task_name]
            now = task_data
            now['statistics']['cpus_limit'] -= 0.1
            delta_t = now['statistics']['timestamp'] - before['statistics']['timestamp']
            cpu_usr_secs = now['statistics']['cpus_user_time_secs'] - before['statistics']['cpus_user_time_secs']
            cpu_sys_secs = now['statistics']['cpus_system_time_secs'] - before['statistics']['cpus_system_time_secs']
            cpu_thr_secs = now['statistics']['cpus_throttled_time_secs'] - before['statistics']['cpus_throttled_time_secs']


            cpu_usr_pct = cpu_usr_secs / delta_t * 100
            cpu_thr_pct = cpu_thr_secs / delta_t * 100
            cpu_usr_pct_mesos = cpu_usr_pct / now['statistics']['cpus_limit']

            #print (f"{task_name} elapsed={delta_t:.3f}, \
#usr_secs={cpu_usr_secs:.3f}, usr_pct={cpu_usr_pct:.3f}%, usr_pct_meso={cpu_usr_pct_mesos:.3f}% ({cpu_usr_pct/100:.3f}, {now['statistics']['cpus_limit']:.3f}), \
#thr_secs={cpu_thr_secs:.3f}, thr_pct={cpu_thr_pct:.3f}%,\
#")

            print_json(before, now)
            CACHE[task_name] = now

        if data:
            print ("")
        await asyncio.sleep(1)


asyncio.get_event_loop().run_until_complete(main())
