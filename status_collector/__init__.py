import aiohttp
import asyncio
import socket as sock

def sorted_ips(raw_ips):
    ips = [sock.inet_pton(sock.AF_INET, ip) for ip in raw_ips]
    ips.sort()
    return [sock.inet_ntop(sock.AF_INET, ip) for ip in ips]

async def get_slave_ip(master_ip):
    session = aiohttp.ClientSession()
    resp = await session.get(f'http://{master_ip}:5050/slaves')
    data = await resp.json()
    result = []
    for slave in data["slaves"]:
        result.append(slave["hostname"])
    await session.close()
    return result



async def main():
    # ip_list = await get_slave_ip("10.168.200.96")
    # ip_list = sorted_ips(ip_list)
    # print (ip_list)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())