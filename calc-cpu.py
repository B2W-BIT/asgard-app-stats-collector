import asyncio
import aiohttp

import os

agent_ip = os.environ.get("AGENT_IP")


CACHE = {}


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

            print (f"{task_name} elapsed={delta_t:.3f}, \
usr_secs={cpu_usr_secs:.3f}, usr_pct={cpu_usr_pct:.3f}%, usr_pct_meso={cpu_usr_pct_mesos:.3f}% ({cpu_usr_pct/100:.3f}, {now['statistics']['cpus_limit']:.3f}), \
thr_secs={cpu_thr_secs:.3f}, thr_pct={cpu_thr_pct:.3f}%,\
")
            CACHE[task_name] = now

        if data:
            print ("")
        await asyncio.sleep(1)


asyncio.get_event_loop().run_until_complete(main())
