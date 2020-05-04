import asyncio
from status_collector import main


asyncio.get_event_loop().run_until_complete(main())
