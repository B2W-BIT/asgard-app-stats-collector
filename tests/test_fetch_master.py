import asynctest
from status_collector import get_slave_ip
from aioresponses import aioresponses

slaves = {
  "slaves": [
    {
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
    },
    {
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
    },
    {
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
    }
  ]
}


class FecthMasterTest(asynctest.TestCase):  
    async def test_get_slaves_ips_list(self):
        with aioresponses() as m:
            m.get('http://10.168.200.96:5050/slaves', payload=slaves)
            slave_ips = await get_slave_ip("10.0.111.43")
            self.assertEquals(slave_ips, ["10.0.111.32:5051", "10.0.111.33:5051", "10.0.111.34:5051"])